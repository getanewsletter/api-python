import unittest
from api import Api
from attribute import Attribute
from attribute_manager import AttributeManager
from httmock import HTTMock, all_requests


class ContactManagerTest(unittest.TestCase):
    def setUp(self):
        gan_token = 'h027MapNNujPH0gV+sXAdmzZTDffHOpJEHaBtrD3NXtNqI4dT3NLXhyTwiZr7PUOGZJNSGv/b9xVyaguX0nDrONGhudPkxtl5EoXrM4SOZHswebpSy2ehh0edrGVF7dVJVZLIlRwgViY3n3/2hMQ5Njp9JFywnOy7gMeaoKw0hYLRbd+wVqvl2oOnspXwGTTcZ9Y+cdP8jIhUUoXOieXst0IXVclAHXa+K1d15gKLcpmXzK+jx14wGEmb4t8MSU'
        self.api = Api(token=gan_token)
        self.attribute_manager = AttributeManager(self.api)

    @all_requests
    def get_existing_attribute_mock(self, url, request):
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
        status_code = 404
        content = '{"detail":"Not found."}'
        return {'status_code': status_code,
                'content': content}

    def test_get_non_existing_attribute(self):
        with HTTMock(self.get_non_existing_attribute_mock):
            self.assertRaises(Exception, self.attribute_manager.get, 'not_existing')

    @all_requests
    def create_attribute_mock(self, url, request):
        status_code = 201
        content = '{"url":"https://api.getanewsletter.com/v3/attributes/attribute2/","name":"Attribute2","code":"attribute2","usage_count":0}'
        return {'status_code': status_code,
                'content': content}

    def test_create_attribute(self):
        attribute = Attribute()
        attribute.name = 'Attribute2'
        with HTTMock(self.create_attribute_mock):
            saved_attribute = self.attribute_manager.save(attribute)
        self.assertTrue(isinstance(saved_attribute, Attribute))
        self.assertEqual(saved_attribute.name, 'Attribute2')

    @all_requests
    def update_existing_attribute_mock(self, url, request):
        status_code = 201
        content = '{"url":"https://api.getanewsletter.com/v3/attributes/changed-attribute/","name":"changed attribute","code":"changed-attribute","usage_count":0}'
        return {'status_code': status_code,
                'content': content}

    def test_update_existing_attribute(self):
        attribute = Attribute()
        attribute.code = 'attribute'
        attribute.name = 'changed attribute'
        with HTTMock(self.update_existing_attribute_mock):
            updated_attribute = self.attribute_manager.save(attribute)
        self.assertTrue(updated_attribute.name, 'changed attribute')
        self.assertTrue(updated_attribute.code, 'changed-attribute')

    @all_requests
    def delete_attribute_mock(self, url, request):
        status_code = 204
        content = ''
        return {'status_code': status_code,
                'content': content}

    def test_delete_attribute(self):
        attribute = Attribute()
        attribute.code = 'changed-attribute'
        with HTTMock(self.delete_attribute_mock):
            self.attribute_manager.delete(attribute)