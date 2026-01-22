from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, foreign, stock
from app.config import settings
from app.core.logger import logger

# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    description="키움증권 REST API를 활용한 트레이딩 시스템",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

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


@app.on_event("startup")
async def startup_event():
    '''앱 시작 시 실행'''
    logger.info(f"{settings.APP_NAME} 시작됨")


@app.on_event("shutdown")
async def shutdown_event():
    '''앱 종료 시 실행'''
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


# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request: Request, exc: StarletteHTTPException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content=APIResponse(success=False, message="HTTP 오류", error=str(exc.detail)).dict()
#     )
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=422,
#         content=APIResponse(success=False, message="검증 실패", error=str(exc)).dict()
#     )
#
# @app.exception_handler(Exception)
# async def general_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content=APIResponse(success=False, message="서버 오류", error=str(exc)).dict()
#     )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )