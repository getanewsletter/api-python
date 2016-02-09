import urlparse


class PaginatedResultSet():
    """
        Class to iterate result pages when searching for entities by query.

        :param manager EntityManager of Entity queried.
        :param data json data to populate class with entities and previous/next
        :raises
    """
    def __init__(self, manager, data):
        self.manager = manager
        self.entities = []
        for result in data.get('results'):
            self.entities.append(self.manager.construct_entity(result).set_persisted())
        self.count = data.get('count')
        self.next_link = data.get('next')
        self.previous_link = data.get('previous')

    def __iter__(self):
        return self

    def url_params_to_dict(self, url):
        """
        :param url: url to get parameters from
        :return: parsed parameters as dict
        """
        params = urlparse.urlparse(url).query
        parsed = urlparse.parse_qsl(params)
        return dict(parsed)

    def next(self):
        """
        Get next page of entity results
        :return: PaginatedResultSet of next result page
        :raises: StopIteration if no next is available
        """
        if self.next_link:
            query_dict = self.url_params_to_dict(self.next_link)
            return self.manager.query(filters=query_dict)
        else:
            raise StopIteration

    def previous(self):
        """
        Get next page of entity results
        :return: PaginatedResultSet of previous result page
        :raises: StopIteration if no previous is available
        """
        if self.previous_link:
            query_dict = self.url_params_to_dict(self.previous_link)
            return self.manager.query(filters=query_dict)
        else:
            raise StopIteration