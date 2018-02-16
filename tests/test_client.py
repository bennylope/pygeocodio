#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_geocodio
----------------------------------

Tests for `geocodio.client` module.
"""


import os
import unittest
import httpretty
from geocodio.client import GeocodioClient, json_points
from geocodio.data import Location, LocationCollection
from geocodio.exceptions import (GeocodioError, GeocodioAuthError,
        GeocodioDataError, GeocodioServerError)


class ClientFixtures(object):

    def setUp(self):
        self.parse_url = "http://api.geocod.io/v1.2/parse"
        self.geocode_url = "http://api.geocod.io/v1.2/geocode"
        self.reverse_url = "http://api.geocod.io/v1.2/reverse"
        self.client = GeocodioClient("1010110101")
        self.err = '{"error": "We are testing"}'


class TestClientErrors(ClientFixtures, unittest.TestCase):

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
                self.parse_url, body=self.err, status=422)
        self.assertRaises(GeocodioDataError, self.client.parse, "")
        httpretty.register_uri(httpretty.GET,
                self.geocode_url, body=self.err, status=422)
        self.assertRaises(GeocodioDataError, self.client.geocode, "")
        httpretty.register_uri(httpretty.POST,
                self.geocode_url, body=self.err, status=422)
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

    @httpretty.activate
    def test_default_error(self):
        """Ensure any other HTTP code raises a general error"""
        httpretty.register_uri(httpretty.GET,
                self.parse_url, body="This does not matter", status=418)
        self.assertRaises(GeocodioError, self.client.parse, "")


class TestClientMethods(ClientFixtures, unittest.TestCase):
    """
    Integration testing for client service methods.
    """

    def setUp(self):
        super(TestClientMethods, self).setUp()
        fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'response/')
        with open(os.path.join(fixtures, 'reverse.json'), 'r') as reverse_json:
            self.single_reverse = reverse_json.read()
        with open(os.path.join(fixtures, 'batch_reverse.json'), 'r') as batch_reverse_json:
            self.batch_reverse = batch_reverse_json.read()

    @httpretty.activate
    def test_reverse_response(self):
        """Ensure reverse geocoding results in a single Location"""
        httpretty.register_uri(httpretty.GET,
                self.reverse_url, body=self.single_reverse, status=200)
        self.assertTrue(isinstance(self.client.reverse((-1, 1)), Location))

    @httpretty.activate
    def test_batch_reverse_response(self):
        """Ensure batch reverse geocoding results in LocationCollection"""
        httpretty.register_uri(httpretty.POST,
                self.reverse_url, body=self.batch_reverse, status=200)
        self.assertTrue(isinstance(self.client.reverse([(-1, 1), (3, 43)]), LocationCollection))
        self.assertTrue(isinstance(self.client.reverse([(-1, 1), (3, 43)], fields=['cd']),
            LocationCollection))

    @httpretty.activate
    def test_bad_field_spec(self):
        """Ensure a bad field name raises a ValueError"""
        httpretty.register_uri(httpretty.POST,
                self.reverse_url, body=self.batch_reverse, status=200)
        self.assertRaises(ValueError, self.client.reverse, (-1, 1), (3, 43), fields=['none'])

    def test_json_points(self):
        """Ensure function returns JSON formatted list of strings"""
        self.assertEqual(
            '["35.9746,-77.9658", "32.87937,-96.63039", "33.83371,-117.836232", "35.417124,-80.678476"]',  # noqa
            json_points([(35.9746000, -77.9658000), (32.8793700, -96.6303900), (33.8337100, -117.8362320), (35.4171240, -80.6784760)]),  # noqa
        )
