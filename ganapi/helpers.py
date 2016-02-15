import urlparse


class PaginatedResultSet(object):
    """
        Class to iterate result pages when searching for entities by query.

        :param manager EntityManager of Entity queried.
        :param data json data to populate class with entities and previous/next
        :raises
    """
    def __init__(self, manager, data):
        self.manager = manager
        self.entities = self.build_entities_list(data.get('results'))
        self.count = data.get('count')
        self.next_link = data.get('next')
        self.previous_link = data.get('previous')

    def __iter__(self):
        return self

    def build_entities_list(self, results):
        """
        :param results: results response of entities from api
        :return: list of constructed entities
        """
        list = []
        for result in results:
            list.append(self.manager.construct_entity(result).set_persisted())
        return list

    @staticmethod
    def url_params_to_dict(url):
        """
        :param url: url to get parameters from
        :return: parsed parameters as dict
        """
        params = urlparse.urlparse(url).query
        parsed = urlparse.parse_qsl(params)
        return dict(parsed)

    def next(self):
        """
        Update Object with next page of entity results and return list of the entities.
        :return: list of entities of next result page
        :raises: StopIteration if no next is available
        """
        if self.next_link:
            query_dict = self.url_params_to_dict(self.next_link)
            next_data = self.manager.query(filters=query_dict, as_json=True)
            self.count = next_data.get('count')
            self.next_link = next_data.get('next')
            self.previous_link = next_data.get('previous')
            self.entities = self.build_entities_list(next_data.get('results'))
            return self.entities
        else:
            raise StopIteration

    def prev(self):
        """
        Update Object with previous page of entity results and return list of the entities.
        :return: PaginatedResultSet of previous result page
        :raises: StopIteration if no previous is available
        """
        if self.previous_link:
            query_dict = self.url_params_to_dict(self.previous_link)
            prev_data = self.manager.query(filters=query_dict, as_json=True)
            self.count = prev_data.get('count')
            self.next_link = prev_data.get('next')
            self.previous_link = prev_data.get('previous')
            self.entities = self.build_entities_list(prev_data.get('results'))
            return self.entities
        else:
            raise StopIteration