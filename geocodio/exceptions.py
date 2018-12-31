class GeocodioError(Exception):
    """General but unknown error from Geocodio"""

    pass


class GeocodioAuthError(GeocodioError):
    """HTTP 403 Access Forbidden, likely due to bad API key"""

    pass


class GeocodioDataError(GeocodioError):
    """HTTP 422 Unprocessable Entity, likely poorly formed address"""

    pass


class GeocodioServerError(GeocodioError):
    """HTTP 500 Server Error, remote server failure"""

    pass
