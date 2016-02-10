import unittest
from api import Api
from attribute import Attribute
from attribute_manager import AttributeManager
from httmock import HTTMock, all_requests
from requests import HTTPError


class ContactManagerTest(unittest.TestCase):
    def setUp(self):
        gan_token = 'h027MapNNujPH0gV+sXAdmzZTDffHOpJEHaBtrD3NXtNqI4dT3NLXhyTwiZr7PUOGZJNSGv/b9xVyaguX0nDrONGhudPkxtl5EoXrM4SOZHswebpSy2ehh0edrGVF7dVJVZLIlRwgViY3n3/2hMQ5Njp9JFywnOy7gMeaoKw0hYLRbd+wVqvl2oOnspXwGTTcZ9Y+cdP8jIhUUoXOieXst0IXVclAHXa+K1d15gKLcpmXzK+jx14wGEmb4t8MSU'
        self.api = Api(token=gan_token)
        self.attribute_manager = AttributeManager(self.api)
        self.start_path = '/v3'

    @all_requests
    def get_existing_attribute_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/attributes/attribute/')
        status_code = 200
        content = '{"url":"https://api.getanewsletter.com/v3/attributes/attribute/","name":"attribute","code":"attribute","usage_count":0}'
        return {'status_code': status_code,
                'content': content}

    def test_get_existing_attribute(self):
        with HTTMock(self.get_existing_attribute_mock):
            attribute = self.attribute_manager.get('attribute')
        self.assertTrue(isinstance(attribute, Attribute))
        self.assertEqual(attribute.name, 'attribute')
        self.assertEqual(attribute.code, 'attribute')

    @all_requests
    def get_non_existing_attribute_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/attributes/non_existing/')
        status_code = 404
        content = '{"detail":"Not found."}'
        return {'status_code': status_code,
                'content': content}

    def test_get_non_existing_attribute(self):
        with HTTMock(self.get_non_existing_attribute_mock):
            self.assertRaises(HTTPError, self.attribute_manager.get, 'non_existing')

    @all_requests
    def create_attribute_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/attributes/')
        self.assertEqual(request.body, '{"name": "Attribute2"}')
        status_code = 201
        content = '{"url":"https://api.getanewsletter.com/v3/attributes/attribute2/","name":"Attribute2","code":"attribute2","usage_count":0}'
        return {'status_code': status_code,
                'content': content}

    def test_create_attribute(self):
        attribute = self.attribute_manager.create()
        attribute.name = 'Attribute2'
        with HTTMock(self.create_attribute_mock):
            saved_attribute = attribute.save()
        self.assertTrue(isinstance(saved_attribute, Attribute))
        self.assertEqual(saved_attribute.name, 'Attribute2')

    @all_requests
    def update_existing_attribute_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/attributes/attribute/')
        self.assertEqual(request.body, '{"name": "changed attribute"}')
        self.assertEqual(request.method, 'PATCH')
        status_code = 201
        content = '{"url":"https://api.getanewsletter.com/v3/attributes/changed-attribute/","name":"changed attribute","code":"changed-attribute","usage_count":0}'
        return {'status_code': status_code,
                'content': content}

    def test_update_existing_attribute(self):
        attribute = self.attribute_manager.create()
        attribute.code = 'attribute'
        attribute.name = 'changed attribute'
        attribute.set_persisted()
        with HTTMock(self.update_existing_attribute_mock):
            updated_attribute = attribute.save()
        self.assertTrue(updated_attribute.name, 'changed attribute')
        self.assertTrue(updated_attribute.code, 'changed-attribute')

    @all_requests
    def delete_attribute_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/attributes/changed-attribute/')
        self.assertEqual(request.method, 'DELETE')
        status_code = 204
        content = ''
        return {'status_code': status_code,
                'content': content}

    def test_delete_attribute(self):
        attribute = self.attribute_manager.create()
        attribute.code = 'changed-attribute'
        with HTTMock(self.delete_attribute_mock):
            attribute.delete()

    @all_requests
    def get_paginated_attributes_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/attributes/')
        self.assertEqual(url.query, '')
        content = '{"count":16,"next":"https://api.getanewsletter.com/v3/attributes/?page=2","previous":null,"results":[{"url":"https://api.getanewsletter.com/v3/attributes/attribute/","name":"attribute","code":"attribute","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/attribute2/","name":"Attribute2","code":"attribute2","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu/","name":"bu","code":"bu","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu1/","name":"bu1","code":"bu1","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu2/","name":"bu2","code":"bu2","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu3/","name":"bu3","code":"bu3","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu4/","name":"bu4","code":"bu4","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu5/","name":"bu5","code":"bu5","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu6/","name":"bu6","code":"bu6","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu7/","name":"bu7","code":"bu7","usage_count":0}]}'
        status_code = 200
        return {'content': content,
                'status_code': status_code}

    def get_paginated_attributes_page2_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/attributes/')
        self.assertEqual(url.query, 'page=2')
        content = '{"count":16,"next":null,"previous":"https://api.getanewsletter.com/v3/attributes/","results":[{"url":"https://api.getanewsletter.com/v3/attributes/bu8/","name":"bu8","code":"bu8","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu9/","name":"bu9","code":"bu9","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu10/","name":"bu10","code":"bu10","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu11/","name":"bu11","code":"bu11","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu12/","name":"bu12","code":"bu12","usage_count":0},{"url":"https://api.getanewsletter.com/v3/attributes/bu13/","name":"bu13","code":"bu13","usage_count":0}]}'
        status_code = 200
        return {'content': content,
                'status_code': status_code}

    def test_get_paginated_attributes(self):
        with HTTMock(self.get_paginated_attributes_mock):
            paginated_result_set = self.attribute_manager.query({})
        self.assertEqual(len(paginated_result_set.entities), 10)
        self.assertTrue(isinstance(paginated_result_set.entities[0], Attribute))

        with HTTMock(self.get_paginated_attributes_page2_mock):
            next_results_list = paginated_result_set.next()
        self.assertEqual(len(next_results_list), 6)

        self.assertEqual(len(paginated_result_set.entities), 6)

        self.assertRaises(StopIteration, paginated_result_set.next)
