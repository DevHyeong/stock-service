from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    '''토큰 발급 요청'''
    grant_type: str = Field(default="client_credentials")
    appkey: str
    secretkey: str


class TokenResponse(BaseModel):
    '''토큰 발급 응답'''
    expires_dt: str
    token_type: str
    token: str


class RevokeTokenRequest(BaseModel):
    '''토큰 폐기 요청'''
    appkey: str
    secretkey: str
    token: str