import unittest
from api import Api, GanException
from contact import Contact
from contact_manager import ContactManager
from httmock import HTTMock, all_requests
from requests import HTTPError

class ContactManagerTest(unittest.TestCase):
    def setUp(self):
        gan_token = 'h027MapNNujPH0gV+sXAdmzZTDffHOpJEHaBtrD3NXtNqI4dT3NLXhyTwiZr7PUOGZJNSGv/b9xVyaguX0nDrONGhudPkxtl5EoXrM4SOZHswebpSy2ehh0edrGVF7dVJVZLIlRwgViY3n3/2hMQ5Njp9JFywnOy7gMeaoKw0hYLRbd+wVqvl2oOnspXwGTTcZ9Y+cdP8jIhUUoXOieXst0IXVclAHXa+K1d15gKLcpmXzK+jx14wGEmb4t8MSU'
        self.api = Api(token=gan_token)
        self.contact_manager = ContactManager(self.api)
        self.start_path = '/v3'

    @all_requests
    def get_contact_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/contacts/tester@example.com/')
        status_code = 200
        content = '{"url":"https://api.getanewsletter.com/v3/contacts/tester@example.com/","first_name":"Test","last_name":"Tester","email":"tester@example.com","created":"2016-02-05T16:21:41","updated":"2016-02-08T14:40:17","attributes":{},"lists":[],"active":true}'
        return {'status_code': status_code,
                'content': content}

    def test_get_existing_contact(self):
        with HTTMock(self.get_contact_mock):
            contact = self.contact_manager.get('tester@example.com')
        contact_obj = {'first_name': u'Test',
                       'last_name': u'Tester',
                       'created': u'2016-02-05T16:21:41',
                       'url': u'https://api.getanewsletter.com/v3/contacts/tester@example.com/',
                       'updated': u'2016-02-05T16:21:41',
                       'lists': [],
                       '_persisted': True,
                       'active': True,
                       'attributes': {},
                       'email': u'tester@example.com'}

        self.assertEqual(contact.first_name, contact_obj['first_name'])
        self.assertEqual(contact.email, contact_obj['email'])
        self.assertTrue(contact.is_persisted())

    @all_requests
    def non_existing_contact_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/contacts/noone@nothing.com/')
        status_code = 404
        content = '{"detail":"Not found."}'
        return {'status_code': status_code,
                'content': content}

    def test_non_existing_contact(self):
        with HTTMock(self.non_existing_contact_mock):
            self.assertRaises(HTTPError, self.contact_manager.get, 'noone@nothing.com')

    @all_requests
    def create_new_contact_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/contacts/')
        self.assertEqual(request.body, '{"attributes": {}, "first_name": "John", "email": "test@example.com", "lists": []}')
        status_code = 201
        content = '{"url":"https://api.getanewsletter.com/v3/contacts/test@example.com/","first_name":"John","last_name":"","email":"test@example.com","created":"2016-02-08T10:38:50","updated":"2016-02-09T09:44:06.399013","attributes":{},"lists":[],"active":true}'
        return {'status_code': status_code,
                'content': content}

    def test_create_new_contact(self):
        contact = self.contact_manager.create()
        contact.email = 'test@example.com'
        contact.first_name = 'John'
        with HTTMock(self.create_new_contact_mock):
            saved_contact = contact.save()
        self.assertTrue(isinstance(saved_contact, Contact))

    @all_requests
    def save_existing_contact_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/contacts/test@example.com/')
        self.assertEqual(request.body, '{"attributes": {}, "first_name": "John", "email": "test@example.com", "lists": []}')
        self.assertEqual(request.method, 'PATCH')
        status_code = 200
        content = '{"url":"https://api.getanewsletter.com/v3/contacts/test@example.com/","first_name":"John","last_name":"","email":"test@example.com","created":"2016-02-08T10:38:50","updated":"2016-02-09T09:48:51.340060","attributes":{},"lists":[],"active":true}'
        return {'status_code': status_code,
                'content': content}

    def test_save_existing_contact(self):
        contact = self.contact_manager.create()
        contact.email = 'test@example.com'
        contact.first_name = 'John'
        contact.set_persisted()
        with HTTMock(self.save_existing_contact_mock):
            saved_contact = contact.save()
        self.assertTrue(isinstance(saved_contact, Contact))

    def test_update_without_email(self):
        contact = self.contact_manager.create()
        contact.first_name = 'John'
        contact.set_persisted()
        self.assertRaises(GanException, contact.save)

    @all_requests
    def overwrite_contact_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/contacts/test@example.com/')
        self.assertEqual(request.method, 'PUT')
        status_code = 200
        content = '{"url":"https://api.getanewsletter.com/v3/contacts/test@example.com/","first_name":"John","last_name":"","email":"test@example.com","created":"2016-02-08T10:38:50","updated":"2016-02-09T10:00:31.428342","attributes":{},"lists":[],"active":true}'
        return {'status_code': status_code,
                'content': content}

    def test_overwrite_contact(self):
        contact = self.contact_manager.create()
        contact.email = 'test@example.com'
        contact.first_name = 'John'
        with HTTMock(self.overwrite_contact_mock):
            overwritten_contact = contact.overwrite()
        self.assertTrue(isinstance(overwritten_contact, Contact))

    @all_requests
    def find_contact_by_query_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/contacts/')
        status_code = 200
        content = '{"count":1,"next":null,"previous":null,"results":[{"url":"https://api.getanewsletter.com/v3/contacts/test@example.com/","first_name":"John","last_name":"","email":"test@example.com","created":"2016-02-08T10:38:50","updated":"2016-02-09T10:00:31","attributes":{},"lists":[],"active":true}]}'
        return {'status_code': status_code,
                'content': content}

    def test_find_contact_by_query(self):
        query = {
            'search_email': 'test@',
            'page': 1
        }
        with HTTMock(self.find_contact_by_query_mock):
            result = self.contact_manager.query(filters=query)
            contacts = result.entities
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].email, 'test@example.com')

    @all_requests
    def delete_contact_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/contacts/new_created@example.com/')
        self.assertEqual(request.method, 'DELETE')
        status_code = 204
        content = ''
        return {'status_code': status_code,
                'content': content}

    def test_delete_contact(self):
        contact = self.contact_manager.create()
        contact.email = 'new_created@example.com'
        with HTTMock(self.delete_contact_mock):
            deleted_contact_response = contact.delete()
            self.assertEqual(deleted_contact_response.status_code, 204)
