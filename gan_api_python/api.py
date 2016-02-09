import json
import requests
import math
from requests.exceptions import RequestException


class Api():
    """
        Handles connection to the API
    """

    """
        The default Api base URI
        :var default_base_uri string
    """
    default_base_uri = 'https://api.getanewsletter.com/v3/'

    """
        Initializes the API connection
        :param string token The security token.
        :param string baseUri (optional) Alternative API base URI.
    """

    def __init__(self, token, base_uri=None):
        """ #The JSON response is going to be deserialized to associative arrays:
            # $json_handler = new Httpful\Handlers\JsonHandler(array('decode_as_array' => true));
            # Httpful\Httpful::register('application/json', $json_handler);
            FIXME IS THIS NEEDED here?
        """
        self.token = token
        self.base_uri = base_uri if base_uri else self.default_base_uri
        self.headers = {'Accept': 'application/json',
                        'Authorization': 'Token {token}'.format(token=self.token),
                        'content-type': 'application/json'
        }

    def call(self, method, resource_path, payload=None):
        """
            Makes a call to the API.

            This method will make the actual API call by the given arguments. It
            will return the response on success (200) or will raise an exception
            on failure.

            :param method string method The HTTP method to use (e.g. GET, POST, etc.).
            :param resource_path string The path to the resource (e.g. contacts/john@example.com/)
            :param payload string The data that is sent to the service. Not used for GET or DELETE.
            :return response The Requests response object from the service.
            :raises Exception
        """
        uri = u'{base_uri}{resource_path}'.format(base_uri=self.base_uri,
                                                  resource_path=resource_path)

        if payload:
            payload = json.dumps(payload)

        if method == 'GET':
            response = requests.get(uri, headers=self.headers, data=payload)
        elif method == 'POST':
            response = requests.post(uri, headers=self.headers, data=payload)
        elif method == 'DELETE':
            response = requests.delete(uri, headers=self.headers, data=payload)
        elif method == 'PUT':
            response = requests.put(uri, headers=self.headers, data=payload)
        elif method == 'PATCH':
            response = requests.patch(uri, headers=self.headers, data=payload)

        if math.floor(response.status_code / 100) != 2:
            raise RequestException(response.status_code, response.content)

        return response