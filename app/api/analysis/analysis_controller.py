from fastapi import APIRouter, Depends, Query, HTTPException
from dependency_injector.wiring import Provide, inject

from app.domain.chart.services.chart_service import ChartService
from app.domain.analysis.services.technical_analysis_service import (
    TechnicalAnalysisService,
)
from app.domain.analysis.dto.response.resistance_support import (
    ResistanceSupportResponse,
    VolumeProfileResponse,
)
from app.containers import Container
from app.schemas.response import APIResponse


router = APIRouter(prefix="/analysis", tags=["기술적 분석"])


# 서비스 의존성 주입
def get_technical_analysis_service() -> TechnicalAnalysisService:
    return TechnicalAnalysisService()


@router.get("/{stock_code}/resistance-support", response_model=APIResponse)
@inject
async def get_resistance_support_levels(
    stock_code: str,
    timeframe: str = Query(
        "day",
        description="차트 타임프레임",
        pattern="^(day|week|month)$"
    ),
    start_dt: str = Query(..., description="분석 시작일 (YYYYMMDD)"),
    end_dt: str = Query(..., description="분석 종료일 (YYYYMMDD)"),
    window: int = Query(
        5,
        ge=2,
        le=20,
        description="고점/저점 판단 윈도우 (전후 비교 봉 개수)"
    ),
    min_touches: int = Query(
        2,
        ge=2,
        le=10,
        description="최소 터치 횟수 (이 값 이상 터치된 가격대만 반환)"
    ),
    tolerance: float = Query(
        0.01,
        ge=0.001,
        le=0.05,
        description="가격 클러스터링 허용 오차 (기본 1%)"
    ),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
    ta_service: TechnicalAnalysisService = Depends(get_technical_analysis_service),
):
    """저항선/지지선 자동 분석

    차트 데이터를 분석하여 주요 저항선과 지지선 가격대를 반환합니다.

    **분석 방법:**
    - 로컬 고점/저점을 찾아 저항/지지 후보 추출
    - 비슷한 가격대를 클러스터링하여 의미 있는 레벨 도출
    - 터치 횟수에 따라 강도 판정 (weak, medium, strong)

    **활용 방법:**
    - `timeframe=day`: 단기 매매 (1~2주)
    - `timeframe=week`: 중기 매매 (1~3개월)
    - `timeframe=month`: 장기 투자 (6개월 이상)

    Args:
        stock_code: 종목코드 (예: 005930)
        timeframe: day(일봉), week(주봉), month(월봉)
        start_dt: 분석 시작일 (예: 20260101)
        end_dt: 분석 종료일 (예: 20260228)
        window: 고점/저점 판단 시 전후 비교할 봉 개수 (기본 5)
        min_touches: 최소 터치 횟수 (기본 2)
        tolerance: 가격 클러스터링 허용 오차 (기본 1%)

    Returns:
        저항선/지지선 분석 결과
    """
    try:
        # 1. 차트 데이터 조회
        chart_data = None
        if timeframe == "day":
            result = await chart_service.get_day_chart(
                stk_cd=stock_code,
                start_dt=start_dt,
                end_dt=end_dt
            )
            chart_data = result.items
        elif timeframe == "week":
            result = await chart_service.get_week_chart(
                stk_cd=stock_code,
                start_dt=start_dt,
                end_dt=end_dt
            )
            chart_data = result.items
        elif timeframe == "month":
            result = await chart_service.get_month_chart(
                stk_cd=stock_code,
                start_dt=start_dt,
                end_dt=end_dt
            )
            chart_data = result.items
        else:
            raise HTTPException(
                status_code=400,
                detail="timeframe은 day, week, month 중 하나여야 합니다."
            )

        if not chart_data:
            return APIResponse(
                success=False,
                message=f"차트 데이터가 없습니다: {stock_code}",
                error="No chart data found"
            )

        # 2. 저항/지지선 분석
        analysis_result = ta_service.find_resistance_support_levels(
            stock_code=stock_code,
            timeframe=timeframe,
            chart_data=chart_data,
            start_dt=start_dt,
            end_dt=end_dt,
            window=window,
            min_touches=min_touches,
            tolerance=tolerance,
        )

        return APIResponse(
            success=True,
            message=f"{stock_code} 저항/지지선 분석 완료",
            data=analysis_result.model_dump()
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(
            success=False,
            message="저항/지지선 분석 실패",
            error=str(e)
        )


@router.get("/{stock_code}/volume-profile", response_model=APIResponse)
@inject
async def get_volume_profile(
    stock_code: str,
    timeframe: str = Query(
        "day",
        description="차트 타임프레임",
        pattern="^(day|week|month)$"
    ),
    start_dt: str = Query(..., description="분석 시작일 (YYYYMMDD)"),
    end_dt: str = Query(..., description="분석 종료일 (YYYYMMDD)"),
    price_bins: int = Query(
        50,
        ge=10,
        le=200,
        description="가격 구간 개수"
    ),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
    ta_service: TechnicalAnalysisService = Depends(get_technical_analysis_service),
):
    """거래량 프로파일 분석

    거래량이 많이 몰린 가격대를 찾아 저항/지지선을 판단합니다.

    **분석 지표:**
    - POC (Point of Control): 최대 거래량이 발생한 가격
    - Value Area: 전체 거래량의 70%가 발생한 가격 범위
    - High Volume Levels: 거래량 상위 20% 가격대

    **활용법:**
    - POC 근처: 강력한 저항/지지선
    - Value Area 상단/하단: 중요한 가격 레벨
    - High Volume Levels: 매물대 = 저항/지지 가능성

    Args:
        stock_code: 종목코드
        timeframe: day(일봉), week(주봉), month(월봉)
        start_dt: 분석 시작일
        end_dt: 분석 종료일
        price_bins: 가격 구간 개수 (기본 50)

    Returns:
        거래량 프로파일 분석 결과
    """
    try:
        # 1. 차트 데이터 조회
        chart_data = None
        if timeframe == "day":
            result = await chart_service.get_day_chart(
                stk_cd=stock_code,
                start_dt=start_dt,
                end_dt=end_dt
            )
            chart_data = result.items
        elif timeframe == "week":
            result = await chart_service.get_week_chart(
                stk_cd=stock_code,
                start_dt=start_dt,
                end_dt=end_dt
            )
            chart_data = result.items
        elif timeframe == "month":
            result = await chart_service.get_month_chart(
                stk_cd=stock_code,
                start_dt=start_dt,
                end_dt=end_dt
            )
            chart_data = result.items
        else:
            raise HTTPException(
                status_code=400,
                detail="timeframe은 day, week, month 중 하나여야 합니다."
            )

        if not chart_data:
            return APIResponse(
                success=False,
                message=f"차트 데이터가 없습니다: {stock_code}",
                error="No chart data found"
            )

        # 2. 거래량 프로파일 분석
        analysis_result = ta_service.find_volume_profile(
            stock_code=stock_code,
            timeframe=timeframe,
            chart_data=chart_data,
            start_dt=start_dt,
            end_dt=end_dt,
            price_bins=price_bins,
        )

        return APIResponse(
            success=True,
            message=f"{stock_code} 거래량 프로파일 분석 완료",
            data=analysis_result.model_dump()
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(
            success=False,
            message="거래량 프로파일 분석 실패",
            error=str(e)
        )
