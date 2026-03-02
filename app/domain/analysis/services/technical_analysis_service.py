from typing import List, Dict, Union
from collections import defaultdict

from app.domain.chart.dto.response.chart_item import (
    DayChartItem,
    WeekChartItem,
    MonthChartItem,
)
from app.domain.analysis.dto.response.resistance_support import (
    PriceLevel,
    ResistanceSupportResponse,
    VolumeProfileLevel,
    VolumeProfileResponse,
)


ChartItem = Union[DayChartItem, WeekChartItem, MonthChartItem]


class TechnicalAnalysisService:
    """기술적 분석 서비스

    차트 데이터를 분석하여 저항선, 지지선, 거래량 프로파일 등을 계산합니다.
    """

    def find_resistance_support_levels(
        self,
        stock_code: str,
        timeframe: str,
        chart_data: List[ChartItem],
        start_dt: str,
        end_dt: str,
        window: int = 5,
        min_touches: int = 2,
        tolerance: float = 0.01,
    ) -> ResistanceSupportResponse:
        """저항선/지지선 자동 탐지

        Args:
            stock_code: 종목코드
            timeframe: 타임프레임 (day, week, month)
            chart_data: OHLCV 차트 데이터
            start_dt: 분석 시작일
            end_dt: 분석 종료일
            window: 고점/저점 판단 시 전후 비교할 봉 개수
            min_touches: 저항/지지선으로 인정할 최소 터치 횟수
            tolerance: 가격 클러스터링 허용 오차 (기본 1%)

        Returns:
            저항/지지선 분석 결과
        """
        if not chart_data or len(chart_data) < window * 2:
            return ResistanceSupportResponse(
                stock_code=stock_code,
                timeframe=timeframe,
                period=f"{start_dt}-{end_dt}",
                current_price=0.0,
                analysis_summary="분석할 데이터가 부족합니다."
            )

        # 1. 현재가 추출
        current_price = float(chart_data[-1].cur_prc)

        # 2. 로컬 고점 찾기 (저항선 후보)
        resistance_candidates = self._find_local_highs(chart_data, window)

        # 3. 로컬 저점 찾기 (지지선 후보)
        support_candidates = self._find_local_lows(chart_data, window)

        # 4. 비슷한 가격대 클러스터링
        resistance_clusters = self._cluster_price_levels(
            resistance_candidates, tolerance
        )
        support_clusters = self._cluster_price_levels(
            support_candidates, tolerance
        )

        # 5. 터치 횟수 계산 및 강도 판정
        resistance_levels = self._calculate_strength(
            resistance_clusters, min_touches
        )
        support_levels = self._calculate_strength(
            support_clusters, min_touches
        )

        # 6. 현재가 기준으로 정렬
        resistance_levels.sort(key=lambda x: x.price)
        support_levels.sort(key=lambda x: x.price, reverse=True)

        # 7. 가장 가까운 저항/지지선 찾기
        nearest_resistance = None
        nearest_support = None

        for level in resistance_levels:
            if level.price > current_price:
                nearest_resistance = level.price
                break

        for level in support_levels:
            if level.price < current_price:
                nearest_support = level.price
                break

        # 8. 분석 요약 생성
        summary = self._generate_summary(
            current_price, nearest_resistance, nearest_support,
            len(resistance_levels), len(support_levels)
        )

        return ResistanceSupportResponse(
            stock_code=stock_code,
            timeframe=timeframe,
            period=f"{start_dt}-{end_dt}",
            current_price=current_price,
            resistance_levels=resistance_levels,
            support_levels=support_levels,
            nearest_resistance=nearest_resistance,
            nearest_support=nearest_support,
            analysis_summary=summary,
        )

    def find_volume_profile(
        self,
        stock_code: str,
        timeframe: str,
        chart_data: List[ChartItem],
        start_dt: str,
        end_dt: str,
        price_bins: int = 50,
    ) -> VolumeProfileResponse:
        """거래량 프로파일 분석

        거래량이 많이 몰린 가격대를 찾아 저항/지지선을 판단합니다.

        Args:
            stock_code: 종목코드
            timeframe: 타임프레임
            chart_data: 차트 데이터
            start_dt: 시작일
            end_dt: 종료일
            price_bins: 가격 구간 개수

        Returns:
            거래량 프로파일 분석 결과
        """
        if not chart_data:
            return VolumeProfileResponse(
                stock_code=stock_code,
                timeframe=timeframe,
                period=f"{start_dt}-{end_dt}",
            )

        # 가격 범위 계산
        min_price = min(float(d.low_pric) for d in chart_data)
        max_price = max(float(d.high_pric) for d in chart_data)
        price_step = (max_price - min_price) / price_bins

        if price_step == 0:
            return VolumeProfileResponse(
                stock_code=stock_code,
                timeframe=timeframe,
                period=f"{start_dt}-{end_dt}",
            )

        # 각 가격 구간별 거래량 집계
        volume_by_bin: Dict[int, int] = defaultdict(int)
        total_volume = 0

        for data in chart_data:
            avg_price = (float(data.high_pric) + float(data.low_pric)) / 2
            volume = int(data.trde_qty)

            bin_index = int((avg_price - min_price) / price_step)
            bin_index = min(bin_index, price_bins - 1)  # 최대값 보정

            volume_by_bin[bin_index] += volume
            total_volume += volume

        # 거래량 상위 구간 추출 (상위 20%)
        sorted_bins = sorted(
            volume_by_bin.items(),
            key=lambda x: x[1],
            reverse=True
        )

        threshold_count = max(int(len(sorted_bins) * 0.2), 5)
        high_volume_bins = sorted_bins[:threshold_count]

        # VolumeProfileLevel 생성
        high_volume_levels = []
        for bin_idx, volume in high_volume_bins:
            price_low = min_price + (bin_idx * price_step)
            price_high = price_low + price_step
            percentage = (volume / total_volume * 100) if total_volume > 0 else 0

            high_volume_levels.append(
                VolumeProfileLevel(
                    price_range=f"{int(price_low)}-{int(price_high)}",
                    volume=volume,
                    percentage=round(percentage, 2),
                )
            )

        # POC (Point of Control) - 최대 거래량 가격
        poc_bin = sorted_bins[0][0] if sorted_bins else 0
        poc_price = min_price + (poc_bin * price_step) + (price_step / 2)

        # Value Area 계산 (거래량 70% 구간)
        value_area_volume = total_volume * 0.7
        accumulated_volume = 0
        value_area_bins = []

        for bin_idx, volume in sorted_bins:
            value_area_bins.append(bin_idx)
            accumulated_volume += volume
            if accumulated_volume >= value_area_volume:
                break

        value_area_high = None
        value_area_low = None
        if value_area_bins:
            max_bin = max(value_area_bins)
            min_bin = min(value_area_bins)
            value_area_high = min_price + ((max_bin + 1) * price_step)
            value_area_low = min_price + (min_bin * price_step)

        return VolumeProfileResponse(
            stock_code=stock_code,
            timeframe=timeframe,
            period=f"{start_dt}-{end_dt}",
            high_volume_levels=high_volume_levels,
            poc=round(poc_price, 2) if poc_price else None,
            value_area_high=round(value_area_high, 2) if value_area_high else None,
            value_area_low=round(value_area_low, 2) if value_area_low else None,
        )

    # ─────────────────────────────────────────────────────────────────────
    # Private Methods
    # ─────────────────────────────────────────────────────────────────────

    def _find_local_highs(
        self, chart_data: List[ChartItem], window: int
    ) -> List[float]:
        """로컬 고점 찾기"""
        highs = []
        data_len = len(chart_data)

        for i in range(window, data_len - window):
            current_high = float(chart_data[i].high_pric)

            # 전후 window개 봉과 비교
            is_local_high = True
            for j in range(i - window, i + window + 1):
                if j == i:
                    continue
                if current_high < float(chart_data[j].high_pric):
                    is_local_high = False
                    break

            if is_local_high:
                highs.append(current_high)

        return highs

    def _find_local_lows(
        self, chart_data: List[ChartItem], window: int
    ) -> List[float]:
        """로컬 저점 찾기"""
        lows = []
        data_len = len(chart_data)

        for i in range(window, data_len - window):
            current_low = float(chart_data[i].low_pric)

            # 전후 window개 봉과 비교
            is_local_low = True
            for j in range(i - window, i + window + 1):
                if j == i:
                    continue
                if current_low > float(chart_data[j].low_pric):
                    is_local_low = False
                    break

            if is_local_low:
                lows.append(current_low)

        return lows

    def _cluster_price_levels(
        self, prices: List[float], tolerance: float
    ) -> Dict[float, int]:
        """비슷한 가격대를 클러스터링하여 터치 횟수 계산

        Returns:
            {대표 가격: 터치 횟수}
        """
        if not prices:
            return {}

        sorted_prices = sorted(prices)
        clusters: Dict[float, List[float]] = {}

        for price in sorted_prices:
            # 기존 클러스터에 속하는지 확인
            matched = False
            for cluster_key in list(clusters.keys()):
                if abs(price - cluster_key) / cluster_key <= tolerance:
                    clusters[cluster_key].append(price)
                    matched = True
                    break

            # 새 클러스터 생성
            if not matched:
                clusters[price] = [price]

        # 각 클러스터의 평균값과 터치 횟수 반환
        result = {}
        for prices_in_cluster in clusters.values():
            avg_price = sum(prices_in_cluster) / len(prices_in_cluster)
            touch_count = len(prices_in_cluster)
            result[avg_price] = touch_count

        return result

    def _calculate_strength(
        self, clusters: Dict[float, int], min_touches: int
    ) -> List[PriceLevel]:
        """가격 레벨의 강도 계산"""
        levels = []

        for price, touches in clusters.items():
            if touches < min_touches:
                continue

            # 강도 판정
            if touches >= 5:
                strength = "strong"
            elif touches >= 3:
                strength = "medium"
            else:
                strength = "weak"

            levels.append(
                PriceLevel(
                    price=round(price, 2),
                    touches=touches,
                    strength=strength,
                )
            )

        return levels

    def _generate_summary(
        self,
        current_price: float,
        nearest_resistance: float | None,
        nearest_support: float | None,
        resistance_count: int,
        support_count: int,
    ) -> str:
        """분석 요약 생성"""
        summary_parts = []

        summary_parts.append(
            f"총 {resistance_count}개의 저항선, {support_count}개의 지지선 발견."
        )

        if nearest_resistance:
            distance_pct = (
                (nearest_resistance - current_price) / current_price * 100
            )
            summary_parts.append(
                f"가장 가까운 저항선: {nearest_resistance:,.0f}원 "
                f"(+{distance_pct:.2f}%)"
            )

        if nearest_support:
            distance_pct = (
                (current_price - nearest_support) / current_price * 100
            )
            summary_parts.append(
                f"가장 가까운 지지선: {nearest_support:,.0f}원 "
                f"(-{distance_pct:.2f}%)"
            )

        if not nearest_resistance and not nearest_support:
            summary_parts.append("현재가 근처에 뚜렷한 저항/지지선이 없습니다.")

        return " ".join(summary_parts)
