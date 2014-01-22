class AccessError(Exception):
    """HTTP 403 Access Forbidden, likely due to bad API key"""
    pass


class UnprocessableError(Exception):
    """HTTP 422 Unprocessable Entity, likely poorly formed address"""
    pass


class ServerError(Exception):
    """HTTP 500 Server Error, remote server failure"""
    pass
