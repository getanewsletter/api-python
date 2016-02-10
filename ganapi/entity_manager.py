import urllib
from helpers import PaginatedResultSet


class EntityManager(object):
    """
    Base entity manager.

    The entity manager is following the Data Mapper pattern and is responsible
    for the mapping of the business objects (Contact, List, etc.) to the REST API.
    by supporting the basic CRUD operations. As an abstract class it need to be
    extended and it's configuration variables set up.
    """
    """
    The base path of the model, i.e. the API endpoint (e.g. 'contacts', 'lists').
    :var base_path string
    """
    base_path = None
    """
    The class of the entity (e.g. 'Contact').
    :var entity_class string
    """
    entity_class = None
    """
    List listing all writable fields. It is required by the default normalize_entity()
    method that is used to clean up the entity before sending it to the API.
    :var writable_fields list
    """
    writable_fields = None
    """
    The name of the field used for model lookup.
    :var lookup_field string
    """
    lookup_field = None

    def __init__(self, api):
        self.api = api

    def get_path(self, id):
        """
        Method used by the entity manager to construct the resource path.

        This method would simply concatenate the lookup id at the end of
        the base path: resource/<id>/. You may have to override it if you
        have an unusual resource path scheme (for example the the subscribers'
        endpoint: lists/<hash>/subscribers/<email>/).

        :param id The id.
        :returns: path string

        """

        return u'{base_path}/{id}/'.format(base_path=str.rstrip(self.base_path),
                                           id=str.rstrip(str(id)))

    def lookup_path(self, entity):
        """
        Method used by the entity manager to construct a resource path from an entity.
        It'll read the content of the lookupField variable to determine which field
        have to be used to construct the path. Again, you may want to override this
        method if you need to construct a path different than resource/<id>/.

        :param entity: The entity to get the path for:
        :return: string The resource path.
        :raises Exception if the lookup field is empty
        """

        lookup_field = self.lookup_field
        if not getattr(entity, lookup_field):
            raise Exception(u'Missing required property: {lookup_field}'.format(lookup_field=lookup_field))

        return self.get_path(getattr(entity, lookup_field))

    def construct_entity(self, data):
        """
         Method used by the entity manager to construct an entity from the API data.

        Given transfer data object (stdClass instance) it have to build and initialize the
        corresponding entity. The default behaviour is to call the entity constructor
        without arguments and fill all entity fields with the supplied data.
        Override this method if your entities require more complex construction procedure.

         :param data: transfer data object from the API.
         :return: The constructed entity.
         """

        entity = self.entity_class(self)
        for property in dir(entity):
            if property in data:
                setattr(entity, property, data[property])
        return entity

    def normalize_entity(self, entity):
        """
        Used to generate a payload for the write operations to the API from an entity.
        This method will use the contents of the writableFields array to get
        only the writable fields from the entity and pack them in an data transfer object
        Override this method if required.

        :param entity: Entity The entity to extract data from.
        :return: data: dict The transfer data dict
        """
        data = {}
        for property in self.writable_fields:
            if getattr(entity, property):
                data[property] = getattr(entity, property)
        return data

    def create(self):
        return self.entity_class(self)

    def get(self, id):
        """
         Retrieves a single entity from the API.

        :param id: string|int The identificator of the entity (e.g. the email of a contact).
        :return: result The constructed entity object
        :raises Exception failure (e.g. the entity is not found).
        """
        resource = self.get_path(id)
        response = self.api.call('GET', resource)
        result = self.construct_entity(response.json())
        result.set_persisted()

        return result

    def save(self, entity, overwrite=False):
        """
        Saves or updates an entity.

        If the $overwrite flag is set, it will make a PUT request to the API.
        It will return the updated/created entity as result.

        :param entity: The entity object to update/save.
        :param overwrite: Set to True if you want
        :return: The updated/created entity.
        :raises RequestException if there is an error from the API
        :raises Exception if the normalixation fails, i.e. missing lookup field.
        """
        data = self.normalize_entity(entity)
        if overwrite:
            response = self.api.call('PUT', self.lookup_path(entity), data)
        else:
            if entity.is_persisted():
                response = self.api.call('PATCH', self.lookup_path(entity), data)
            else:
                uri = u'{base_path}/'.format(base_path=str.rstrip(self.base_path, '/'))
                response = self.api.call('POST', uri, data)

        result = self.construct_entity(response.json())
        result.set_persisted()
        return result

    def overwrite(self, entity):
        """
        Overwrites an entity.

        It internally calls save() with the overwrite flag set.

        :param entity
        :returns The created entity.
        :raises RequestException if there is an error from the API.
        :raises Exception if the normalization fails, i.e. missing lookup field.
        """
        return self.save(entity, True)

    def query(self, filters=dict(), as_json=False):
        """
        Low level method for making search queries.

        Used to get collections of entities based on a search query.
        The query parameters are specific to the entity type, except
        page and paginate_by which are common.

        :param filters dict of query parameters (e.g. {'search_email': 'test@', 'page': 2})
        :param as_json default False set to True to return json
        :returns class PaginatedResultSet which can iterate over pages PaginatedResultSet.entities is the current page list of entities.
        :raises RequestException if there is an error from the API.
        """
        uri = u'{base_path}/?{encoded_filters}'.format(base_path=str.rstrip(self.base_path),
                                                       encoded_filters=urllib.urlencode(filters))
        response = self.api.call('GET', uri)

        if as_json:
            return response.json()
        return PaginatedResultSet(self, response.json())

    def delete(self, entity):
        """
         Deletes an entity.

         :param entity The entity to delete.
         :raises RequestException if there is an error from the API.
        """
        return self.api.call('DELETE', self.lookup_path(entity))