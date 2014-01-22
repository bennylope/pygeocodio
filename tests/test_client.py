#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_geocodio
----------------------------------

Tests for `geocodio.client` module.
"""


import unittest
import httpretty
from geocodio.client import GeocodioClient
from geocodio.exceptions import (GeocodioAuthError, GeocodioDataError,
        GeocodioServerError)


class TestClientErrors(unittest.TestCase):

    def setUp(self):
        self.parse_url = "http://api.geocod.io/v1/parse"
        self.geocode_url = "http://api.geocod.io/v1/geocode"
        self.client = GeocodioClient("1010110101")

    @httpretty.activate
    def test_auth_error(self):
        """Ensure an HTTP 403 code raises GeocodioAuthError"""
        httpretty.register_uri(httpretty.GET,
                self.parse_url, body="This does not matter", status=403)
        self.assertRaises(GeocodioAuthError, self.client.parse, "")
        httpretty.register_uri(httpretty.GET,
                self.geocode_url, body="This does not matter", status=403)
        self.assertRaises(GeocodioAuthError, self.client.geocode, "")
        httpretty.register_uri(httpretty.POST,
                self.geocode_url, body="This does not matter", status=403)
        self.assertRaises(GeocodioAuthError, self.client.geocode, [""])

    @httpretty.activate
    def test_data_error(self):
        """Ensure an HTTP 422 code raises GeocodioDataError"""
        httpretty.register_uri(httpretty.GET,
                self.parse_url, body="This does not matter", status=422)
        self.assertRaises(GeocodioDataError, self.client.parse, "")
        httpretty.register_uri(httpretty.GET,
                self.geocode_url, body="This does not matter", status=422)
        self.assertRaises(GeocodioDataError, self.client.geocode, "")
        httpretty.register_uri(httpretty.POST,
                self.geocode_url, body="This does not matter", status=422)
        self.assertRaises(GeocodioDataError, self.client.geocode, [""])

    @httpretty.activate
    def test_server_error(self):
        """Ensure an HTTP 500 code raises GeocodioServerError"""
        httpretty.register_uri(httpretty.GET,
                self.parse_url, body="This does not matter", status=500)
        self.assertRaises(GeocodioServerError, self.client.parse, "")
        httpretty.register_uri(httpretty.GET,
                self.geocode_url, body="This does not matter", status=500)
        self.assertRaises(GeocodioServerError, self.client.geocode, "")
        httpretty.register_uri(httpretty.POST,
                self.geocode_url, body="This does not matter", status=500)
        self.assertRaises(GeocodioServerError, self.client.geocode, [""])
