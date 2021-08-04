from http import HTTPStatus
import base64
import unittest
import json
from mock import patch
from pathlib import Path
from nest.json_parser import JsonParser
from app import app


class ViewTestCase(unittest.TestCase):
    def setUp(self):

        path = Path(__file__) / '..' / 'test_json.json'
        with open(path.resolve()) as json_file:
            self.json = json.load(json_file)

        path = Path(__file__) / '..' / 'parsed_json.json'
        with open(path.resolve()) as json_file:
            self.parsed_json = json.load(json_file)

        self.three_key_dict = self.parsed_json.get("three_key")
        self.two_key_dict = self.parsed_json.get("two_key")
        self.one_key_dict = self.parsed_json.get("one_key")
        self.client = app.test_client()
        auth = base64.b64encode("admin:admin".encode()).decode()
        self.auth_headers = {'Authorization': f'Basic {auth}'}

    def test_no_args(self):
        parser = JsonParser(self.json, [])
        result = parser.parse()
        self.assertEqual(result, self.json)

    @patch('nest.json_parser.logging')
    def test_invalid_arg(self, mock_logging):
        parser = JsonParser(self.json, ['invalid_arg'])
        with self.assertRaises(Exception) as ex:
            parser.parse()
        mock_logging.error.assert_called_once_with('Key error: Key does not exist in json object')

    def test_no_json(self):
        parser = JsonParser({}, ['currency'])
        result = parser.parse()
        self.assertEqual(result, {})

    @patch('nest.json_parser.logging')
    def test_invalid_json(self, mock_logging):
        parser = JsonParser(str(self.json), ['currency'])
        with self.assertRaises(Exception) as ex:
            parser.parse()
        mock_logging.error.assert_called_once_with('Incorrect input type')

    def test_two_key(self):
        parser = JsonParser(self.json, ['city', 'currency'])
        result = parser.parse()
        self.assertEqual(result, self.two_key_dict)

    def test_one_key(self):
        parser = JsonParser(self.json, ['country'])
        result = parser.parse()
        self.assertEqual(result, self.one_key_dict)

    def test_three_key(self):
        parser = JsonParser(self.json, ['currency', 'country', 'city'])
        result = parser.parse()
        self.assertEqual(result, self.three_key_dict)

    def test_parser_resource_post_ok(self):
        response = self.client.post(f'/parse?keys=currency, country, city', json=self.json, headers=self.auth_headers)
        self.assertEqual(response.json, self.three_key_dict)
        assert response.status_code == HTTPStatus.OK

    def test_parser_resource_post_bad_request(self):
        response = self.client.post(f'/parse', data='bad_json', headers=self.auth_headers)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        response = self.client.post(f'/parse', json='bad_json', headers=self.auth_headers)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_parser_resource_post_unauthorized(self):
        response = self.client.post(f'/parse')
        assert response.status_code == HTTPStatus.UNAUTHORIZED
