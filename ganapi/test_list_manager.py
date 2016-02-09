import unittest
from api import Api
from list import List
from list_manager import ListManager
from httmock import HTTMock, all_requests


class ListManagerTest(unittest.TestCase):
    def setUp(self):
        gan_token = 'h027MapNNujPH0gV+sXAdmzZTDffHOpJEHaBtrD3NXtNqI4dT3NLXhyTwiZr7PUOGZJNSGv/b9xVyaguX0nDrONGhudPkxtl5EoXrM4SOZHswebpSy2ehh0edrGVF7dVJVZLIlRwgViY3n3/2hMQ5Njp9JFywnOy7gMeaoKw0hYLRbd+wVqvl2oOnspXwGTTcZ9Y+cdP8jIhUUoXOieXst0IXVclAHXa+K1d15gKLcpmXzK+jx14wGEmb4t8MSU'
        self.api = Api(token=gan_token)
        self.list_manager = ListManager(self.api)

    @all_requests
    def get_list_mock(self, url, request):
        status_code = 200
        content = '{"url":"https://api.getanewsletter.com/v3/lists/2anfLVM/","hash":"2anfLVM","name":"Test list","active_subscribers_count":1,"subscribers_count":1,"sender":"rasmus.lager@chas.se","email":"rasmus.lager@chas.se","description":"A list that you can use for sending out newsletter tests","created":"2016-02-05T13:38:26","subscribers":"https://api.getanewsletter.com/v3/lists/2anfLVM/subscribers/","responders_count":0,"responders":[]}'
        return {'status_code': status_code,
                'content': content}

    def test_get_list(self):
        with HTTMock(self.get_list_mock):
            list = self.list_manager.get('2anfLVM')
        self.assertTrue(isinstance(list, List))
        self.assertTrue(list.hash, '2anfLVM')
        self.assertTrue(list.is_persisted())

    def test_update_without_hash(self):
        # Expects exception
        list = List()
        list.name = 'list'
        list.sender = 'John Doe'
        list.set_persisted()
        self.assertRaises(Exception, self.list_manager.save, list)

    @all_requests
    def create_new_list_mock(self, url, request):
        status_code = 201
        content = '{"url":"https://api.getanewsletter.com/v3/lists/onZQWLL/","hash":"onZQWLL","name":"list","active_subscribers_count":0,"subscribers_count":0,"sender":"John Doe","email":"testare@example.com","description":"","created":"2016-02-09T10:25:11.190447","subscribers":"https://api.getanewsletter.com/v3/lists/onZQWLL/subscribers/","responders_count":0,"responders":[]}'
        return {'status_code': status_code,
                'content': content}

    def test_create_new_list(self):
        new_list = List()
        new_list.name = 'list'
        new_list.sender = 'John Doe'
        new_list.email = 'testare@example.com'
        with HTTMock(self.create_new_list_mock):
            saved_list = self.list_manager.save(new_list)
        self.assertTrue(isinstance(saved_list, List))
        self.assertEqual(saved_list.name, 'list')

    @all_requests
    def update_list_mock(self, url, request):
        status_code = 200
        content = '{"url":"https://api.getanewsletter.com/v3/lists/onZQWLL/","hash":"onZQWLL","name":"list two","active_subscribers_count":0,"subscribers_count":0,"sender":"sender","email":"testare@example.com","description":"","created":"2016-02-09T10:25:11","subscribers":"https://api.getanewsletter.com/v3/lists/onZQWLL/subscribers/","responders_count":0,"responders":[]}'
        return {'status_code': status_code,
                'content': content}

    def test_update_list(self):
        new_list = List()
        new_list.hash = 'onZQWLL'
        new_list.name = 'list two'
        new_list.sender = 'sender'
        new_list.set_persisted()
        with HTTMock(self.update_list_mock):
            saved_list = self.list_manager.save(new_list)
        self.assertEqual(saved_list.name, 'list two')
        self.assertEqual(saved_list.hash, new_list.hash)


    @all_requests
    def overwrite_list_mock(self, url, request):
        status_code = 200
        content = '{"url":"https://api.getanewsletter.com/v3/lists/onZQWLL/","hash":"onZQWLL","name":"overwritten list","active_subscribers_count":0,"subscribers_count":0,"sender":"John","email":"test@example.com","description":"","created":"2016-02-09T10:25:11","subscribers":"https://api.getanewsletter.com/v3/lists/onZQWLL/subscribers/","responders_count":0,"responders":[]}'
        return {'status_code': status_code,
                'content': content}

    def test_overwrite_list(self):
        known_hash = 'onZQWLL'
        new_list = List()
        new_list.hash = known_hash
        new_list.name = 'overwritten list'
        new_list.email = 'test@example.com'
        new_list.sender = 'John'
        with HTTMock(self.overwrite_list_mock):
            overwritten_list = self.list_manager.overwrite(new_list)
        self.assertEqual(overwritten_list.sender, 'John')

    @all_requests
    def delete_list_mock(self, url, request):
        status_code = 204
        content = ''
        return {'status_code': status_code,
                'content': content}

    def test_delete_list(self):
        new_list = List()
        new_list.hash = 'onZQWLL'
        with HTTMock(self.delete_list_mock):
            response = self.list_manager.delete(new_list)
        self.assertEqual(response.status_code, 204)
