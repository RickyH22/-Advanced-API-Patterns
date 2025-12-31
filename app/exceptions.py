"""Custom exceptions for the API"""

class APIException(Exception):
    """Base API exception"""
    
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code or f"ERR_{status_code}"
        super().__init__(self.detail)

class BadRequestException(APIException):
    """400 Bad Request"""
    def __init__(self, detail: str, error_code: str = "BAD_REQUEST"):
        super().__init__(400, detail, error_code)

class UnauthorizedException(APIException):
    """401 Unauthorized"""
    def __init__(self, detail: str = "Not authenticated", error_code: str = "UNAUTHORIZED"):
        super().__init__(401, detail, error_code)

class ForbiddenException(APIException):
    """403 Forbidden"""
    def __init__(self, detail: str = "Not enough permissions", error_code: str = "FORBIDDEN"):
        super().__init__(403, detail, error_code)

class NotFoundException(APIException):
    """404 Not Found"""
    def __init__(self, detail: str = "Resource not found", error_code: str = "NOT_FOUND"):
        super().__init__(404, detail, error_code)

class TooManyRequestsException(APIException):
    """429 Too Many Requests"""
    def __init__(self, detail: str = "Rate limit exceeded", error_code: str = "RATE_LIMIT_EXCEEDED", retry_after: int = 60):
        super().__init__(429, detail, error_code)
        self.retry_after = retry_after
