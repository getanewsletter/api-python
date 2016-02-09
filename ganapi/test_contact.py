from api import Api
from contact import Contact
from contact_manager import ContactManager
from list_manager import ListManager
import unittest
from httmock import HTTMock, all_requests


class ContactTest(unittest.TestCase):
    def setUp(self):
        gan_token = 'h027MapNNujPH0gV+sXAdmzZTDffHOpJEHaBtrD3NXtNqI4dT3NLXhyTwiZr7PUOGZJNSGv/b9xVyaguX0nDrONGhudPkxtl5EoXrM4SOZHswebpSy2ehh0edrGVF7dVJVZLIlRwgViY3n3/2hMQ5Njp9JFywnOy7gMeaoKw0hYLRbd+wVqvl2oOnspXwGTTcZ9Y+cdP8jIhUUoXOieXst0IXVclAHXa+K1d15gKLcpmXzK+jx14wGEmb4t8MSU'
        self.api = Api(token=gan_token)
        self.contact_manager = ContactManager(self.api)
        self.list_manager = ListManager(self.api)
        self.start_path = '/v3'

    @all_requests
    def contact_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/contacts/')
        payload = '{"attributes": {}, "email": "tester@example.com", "lists": []}'
        self.assertEqual(request.body, payload)
        content = '{"url":"https://api.getanewsletter.com/v3/contacts/tester@example.com/","first_name":"","last_name":"","email":"tester@example.com","created":"2016-02-08T14:48:24","updated":"2016-02-09T09:09:28.878356","attributes":{},"lists":[],"active":true}'
        return {'status_code': 201,
                'content': content}

    @all_requests
    def subscribed_contact_mock(self, url, request):
        self.assertEqual(url.path, self.start_path + '/contacts/tester@example.com/')
        content = '{"url":"https://api.getanewsletter.com/v3/contacts/tester@example.com/","first_name":"","last_name":"","email":"tester@example.com","created":"2016-02-08T14:48:24","updated":"2016-02-09T09:17:10.869772","attributes":{},"lists":[{"subscription_cancelled":null,"subscription_id":136363367,"hash":"2anfLVM","name":"Test list","subscription_created":"2016-02-09T08:17:10Z"}],"active":true}'
        status_code = 200
        return {'status_code': status_code,
                'content': content}

    def test_subscribe_to_list(self):
        new_contact = Contact()
        new_contact.email = 'tester@example.com'
        with HTTMock(self.contact_mock):
            new_contact = self.contact_manager.save(new_contact)
        self.assertEqual(new_contact.lists, [])

        list = self.list_manager.construct_entity({'hash': '2anfLVM'})
        new_contact.subscribe_to(list)
        self.assertEqual(len(new_contact.lists), 1)
        with HTTMock(self.subscribed_contact_mock):
            saved_contact = self.contact_manager.save(new_contact)
        self.assertEqual(saved_contact.lists[0]['hash'], '2anfLVM')