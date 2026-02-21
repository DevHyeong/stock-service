from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import rank_controller, stock_controller
from app.api.v1 import auth, foreign, stock, market, sector, trading, chart
from app.config import settings
from app.containers import Container
from app.core.logger import logger
from app.batch.scheduler import start_scheduler, shutdown_scheduler


def create_app() -> FastAPI:
    # Container 초기화
    container = Container()

    # FastAPI 앱 생성
    app = FastAPI(
        title=settings.APP_NAME,
        description="키움증권 REST API를 활용한 트레이딩 시스템",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Container를 앱에 연결
    app.container = container

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
    app.include_router(foreign.router, prefix=settings.API_V1_PREFIX)
    app.include_router(stock.router, prefix=settings.API_V1_PREFIX)
    app.include_router(market.router, prefix=settings.API_V1_PREFIX)
    app.include_router(sector.router, prefix=settings.API_V1_PREFIX)
    app.include_router(trading.router, prefix=settings.API_V1_PREFIX)
    app.include_router(chart.router, prefix=settings.API_V1_PREFIX)
    app.include_router(rank_controller.router, prefix=settings.API_V1_PREFIX)
    app.include_router(stock_controller.router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    '''앱 시작 시 실행'''
    logger.info(f"{settings.APP_NAME} 시작됨")

    # 배치 스케줄러 시작
    if settings.ENABLE_BATCH_SCHEDULER:
        start_scheduler()
        logger.info("배치 스케줄러 활성화됨")


@app.on_event("shutdown")
async def shutdown_event():
    '''앱 종료 시 실행'''
    # 배치 스케줄러 종료
    if settings.ENABLE_BATCH_SCHEDULER:
        shutdown_scheduler()

    logger.info(f"{settings.APP_NAME} 종료됨")


@app.get("/")
async def root():
    '''루트 엔드포인트'''
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    '''헬스 체크'''
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
