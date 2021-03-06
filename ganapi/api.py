import json
import requests
from gan_exception import GanException


class Api(object):
    """
        Handles connection to the API
    """

    """
        The default Api base URI
        :var default_base_uri string
    """
    default_base_uri = 'https://api.getanewsletter.com/v3/'

    """
        The amount of entities to get in each request while using all
        :var batch_size int
    """
    batch_size = 25
    """
        Initializes the API connection
        :param string token The security token.
        :param string base_uri (optional) Alternative API base URI.
    """

    def __init__(self, token, base_uri=None):
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
            :raises GanException in case of invalid HTTP method or HTTPError
        """
        uri = u'{base_uri}{resource_path}'.format(base_uri=self.base_uri,
                                                  resource_path=resource_path)

        if payload:
            payload = json.dumps(payload)

        if method == 'GET':
            response = requests.get(uri, headers=self.headers)
        elif method == 'POST':
            response = requests.post(uri, headers=self.headers, data=payload)
        elif method == 'DELETE':
            response = requests.delete(uri, headers=self.headers)
        elif method == 'PUT':
            response = requests.put(uri, headers=self.headers, data=payload)
        elif method == 'PATCH':
            response = requests.patch(uri, headers=self.headers, data=payload)
        else:
            raise GanException(u'Invalid HTTP method',
                               u'{method} is not a valid HTTP method! Valid HTTP methods are GET, POST, DELETE, PUT, PATCH.'.format(method=method))

        response.raise_for_status()

        return response
