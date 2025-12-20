class KiwoomAPIException(Exception):
    '''키움 API 관련 예외'''
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationException(KiwoomAPIException):
    '''인증 실패 예외'''
    def __init__(self, message: str = "인증에 실패했습니다"):
        super().__init__(message, status_code=401)


class TokenExpiredException(KiwoomAPIException):
    '''토큰 만료 예외'''
    def __init__(self, message: str = "토큰이 만료되었습니다"):
        super().__init__(message, status_code=401)