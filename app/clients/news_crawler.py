import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from abc import ABC, abstractmethod
from urllib.parse import urljoin, quote
from datetime import datetime

logger = logging.getLogger(__name__)

# --- Strategy Interface and Concrete Implementations ---

class NewsScraperStrategy(ABC):
    """Abstract base class for news scraping strategies."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def _get_full_url(self, path: str) -> str:
        """Converts a relative URL to an absolute URL."""
        return urljoin(self.base_url, path)

    @abstractmethod
    def scrape(self, soup: BeautifulSoup) -> List[Dict]:
        """Parses the BeautifulSoup object to extract news articles."""
        pass
        
    @abstractmethod
    def get_search_url(self, query: str, **kwargs) -> str:
        """Constructs the search URL for the news source."""
        pass


class GoogleNewsScraperStrategy(NewsScraperStrategy):
    """Scraping strategy for Google News RSS feed."""

    def __init__(self):
        super().__init__("https://news.google.com")

    def get_search_url(self, query: str, **kwargs) -> str:
        language = kwargs.get("language", "ko")
        country = kwargs.get("country", "KR")
        encoded_query = quote(query)
        # Use RSS feed for more reliable parsing
        return f"{self.base_url}/rss/search?q={encoded_query}&hl={language}&gl={country}&ceid={country}:{language}"

    def scrape(self, soup: BeautifulSoup) -> List[Dict]:
        news_articles = []
        # Parse RSS feed
        items = soup.find_all('item')
        
        for item in items:
            title_tag = item.find('title')
            link_tag = item.find('link')
            source_tag = item.find('source')
            pub_date_tag = item.find('pubdate')

            if not title_tag or not link_tag:
                continue

            title = title_tag.text.strip()
            link = link_tag.text.strip()
            source = source_tag.text.strip() if source_tag else "N/A"
            published_time = pub_date_tag.text.strip() if pub_date_tag else "N/A"

            news_articles.append({
                "title": title,
                "link": link,
                "source": source,
                "time": published_time
            })
            
        return news_articles


class NaverNewsScraperStrategy(NewsScraperStrategy):
    """Scraping strategy for Naver News.
    
    Note: Naver News requires JavaScript rendering for modern pages.
    This implementation provides a basic structure but may not work
    without using a headless browser like Selenium or Playwright.
    Consider using Google News RSS or Naver API for production use.
    """

    def __init__(self):
        super().__init__("https://search.naver.com")

    def get_search_url(self, query: str, **kwargs) -> str:
        sort = kwargs.get("sort", "1")  # 0: relevance, 1: recent
        encoded_query = quote(query)
        # Using display parameter to limit results
        return f"{self.base_url}/search.naver?where=news&query={encoded_query}&sort={sort}&start=1"

    def scrape(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Note: Naver uses JavaScript to load content dynamically.
        This simple scraper may return limited results.
        For production use, consider:
        1. Using Selenium/Playwright for JavaScript rendering
        2. Using Naver Search API (requires API key)
        3. Using Google News RSS as primary source
        """
        news_articles = []
        
        # Try multiple selectors for compatibility
        selectors = [
            'div.news_area',
            'div.api_subject_bx a',
            'div.news_info a',
            '.list_news a.news_tit'
        ]
        
        for selector in selectors:
            items = soup.select(selector)
            if items:
                logger.info(f"Found {len(items)} items with selector: {selector}")
                break
        
        # Filter out non-news links
        skip_patterns = ['Keep', '저장', '바로가기', '선정', '구독', 'static', 'keep.naver']
        
        for item in items[:50]:  # Check more items to get actual news
            if item.name != 'a':
                item = item.find('a')
            
            if not item or not item.get('href'):
                continue

            title = item.get('title', item.text.strip())
            link = item.get('href', '')
            
            # Skip non-news items
            if not title or len(title) < 10:
                continue
            
            # Skip UI elements and promotional links
            if any(pattern in title for pattern in skip_patterns):
                continue
            
            if any(pattern in link for pattern in skip_patterns):
                continue
            
            # Only include proper news article links
            if not link.startswith('http'):
                continue

            news_articles.append({
                "title": title,
                "link": link,
                "source": "Naver News",
                "time": "N/A"
            })
            
            if len(news_articles) >= 20:  # Limit to 20 valid articles
                break
            
        return news_articles

# --- Main Crawler (Context) ---

class NewsCrawler:
    """A flexible news crawler that uses different strategies for different sources."""

    def __init__(self):
        self.strategies: Dict[str, NewsScraperStrategy] = {
            "google": GoogleNewsScraperStrategy(),
            "naver": NaverNewsScraperStrategy(),
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def get_strategy(self, source: str) -> Optional[NewsScraperStrategy]:
        """Returns the strategy for the given source."""
        strategy = self.strategies.get(source)
        if not strategy:
            logger.error(f"No strategy found for source: {source}")
        return strategy

    def crawl(self, stock_name: str, source: str = "google", **kwargs) -> List[Dict]:
        """
        Crawls a news source for articles related to the given stock name
        using a specified strategy.

        Args:
            stock_name: The name of the stock to search for.
            source: The news source to use (e.g., 'google').
            **kwargs: Additional arguments for the strategy (e.g., language, country).

        Returns:
            A list of news articles.
        """
        strategy = self.get_strategy(source)
        if not strategy:
            return []

        search_url = strategy.get_search_url(stock_name, **kwargs)
        
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Use 'xml' parser for RSS feeds, 'html.parser' for HTML
            parser = 'xml' if 'rss' in search_url else 'html.parser'
            soup = BeautifulSoup(response.text, parser)
            
            articles = strategy.scrape(soup)
            logger.info(f"Successfully crawled {len(articles)} articles from {source}")
            return articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error crawling {search_url}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during crawling: {e}", exc_info=True)
            
        return []

# --- Example Usage ---

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    crawler = NewsCrawler()
    stock_name_to_search = "삼성전자"
    
    print(f"\n{'='*60}")
    print(f"Searching for: '{stock_name_to_search}'")
    print(f"{'='*60}\n")
    
    # Test Google News (RSS feed)
    print(f"--- Google News (RSS) ---")
    google_news = crawler.crawl(stock_name_to_search, source="google", language="ko", country="KR")
    
    if google_news:
        for i, article in enumerate(google_news[:5], 1):
            print(f"  {i}. {article['title']}")
            print(f"     Source: {article['source']}")
            print(f"     Time: {article['time']}")
            print(f"     Link: {article['link'][:80]}...")
            print()
    else:
        print("  No news found.\n")
    
    # Test Naver News
    print(f"--- Naver News ---")
    naver_news = crawler.crawl(stock_name_to_search, source="naver", sort="1")
    
    if naver_news:
        for i, article in enumerate(naver_news[:5], 1):
            print(f"  {i}. {article['title']}")
            print(f"     Source: {article['source']}")
            print(f"     Time: {article['time']}")
            print(f"     Link: {article['link'][:80]}...")
            print()
    else:
        print("  No news found.\n")
    
    print(f"{'='*60}")