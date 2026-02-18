from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    async def __aenter__(self):
        await self._begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self._close()

    @abstractmethod
    async def _begin(self):
        """세션 및 리포지토리 초기화"""

    @abstractmethod
    async def _close(self):
        """세션 정리"""

    @abstractmethod
    async def commit(self):
        """트랜잭션 커밋"""

    @abstractmethod
    async def rollback(self):
        """트랜잭션 롤백"""
