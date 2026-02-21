from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# 비동기 엔진 생성
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    future=True,
    pool_pre_ping=True
)

# 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Base 클래스 (모델 정의용)
Base = declarative_base()

# 의존성 주입용 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# 배치 작업용 세션 생성 함수
async def get_session():
    """배치 작업에서 사용하는 세션 생성 함수"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# 테이블 초기화 (개발용)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)