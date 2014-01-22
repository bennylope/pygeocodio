class GeocodioError(Exception):
    """General but unknown error from Geocodio"""
    pass


class GeocodioAuthError(Exception):
    """HTTP 403 Access Forbidden, likely due to bad API key"""
    pass


class GeocodioDataError(Exception):
    """HTTP 422 Unprocessable Entity, likely poorly formed address"""
    pass


class GeocodioServerError(Exception):
    """HTTP 500 Server Error, remote server failure"""
    pass
