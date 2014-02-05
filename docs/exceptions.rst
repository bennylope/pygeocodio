==========
Exceptions
==========

The Geocod.io service may respond with errors, so `pygeocodio` provides some
names exceptions that can be used to identify specific error types. The
Geocod.io documentation lists the following expected responses::

    200 OK Hopefully you will see this most of the time. Note that this status code will also be returned even though no geocoding results were available
    403 Forbidden Invalid API key or other reason why access is forbidden
    422 Unprocessable Entity A client error prevented the request from executing succesfully (e.g. invalid address provided). A JSON object will be returned with an error key containing a full error message
    500 Server Error Hopefully you will never see this...it means that something went wrong in our end. Whoops.

To handle these:

* An HTTP 403 error raises a `GeocodioAuthError`
* An HTTP 422 error raises a `GeocodioDataError` and the error message will be
  reported through the exception
* An HTTP 5xx error raises a `GeocodioServerError`
* An unmatched non-200 response will simply raise `GeocodioError`
