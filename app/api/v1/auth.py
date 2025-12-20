from fastapi import APIRouter, Depends
from app.models.response import APIResponse
from app.models.auth import TokenResponse
from app.services.auth_service import AuthService
from app.api.deps import get_auth_service

router = APIRouter(prefix="/auth", tags=["인증"])


@router.post("/token", response_model=APIResponse[TokenResponse])
async def get_token(
        auth_service: AuthService = Depends(get_auth_service)
):
    '''접근 토큰 발급'''
    try:
        result = await auth_service.get_token()
        return APIResponse(
            success=True,
            message="토큰이 발급되었습니다",
            data=result
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="토큰 발급 실패",
            error=str(e)
        )


@router.delete("/token")
async def revoke_token(
        auth_service: AuthService = Depends(get_auth_service)
):
    '''접근 토큰 폐기'''
    try:
        result = await auth_service.revoke_token()
        return APIResponse(
            success=True,
            message=result["message"],
            data=None
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="토큰 폐기 실패",
            error=str(e)
        )