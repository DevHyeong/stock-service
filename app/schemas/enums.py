from enum import Enum


class MarketCode(str, Enum):
    """시장구분 코드

    키움 API에서 사용하는 시장구분 코드입니다.
    자세한 내용은 doc/market_code.md 참조
    """

    # 주요 시장
    KOSPI = "0"           # 코스피
    KOSDAQ = "10"         # 코스닥
    K_OTC = "30"          # K-OTC
    KONEX = "50"          # 코넥스

    # ETN/ETF
    ETN = "60"            # ETN
    ETN_LOSS_LIMIT = "70" # 손실제한 ETN
    ETN_VOLATILITY = "90" # 변동성 ETN
    ETF = "8"             # ETF

    # 기타
    GOLD = "80"           # 금현물
    INFRA = "2"           # 인프라투융자
    ELW = "3"             # ELW
    MUTUAL_FUND = "4"     # 뮤추얼펀드
    STOCK_WARRANT = "5"   # 신주인수권
    REITS = "6"           # 리츠종목
    WARRANT_CERT = "7"    # 신주인수권증서
    HIGH_YIELD = "9"      # 하이일드펀드
