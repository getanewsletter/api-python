from contact import Contact
from entity_manager import EntityManager
from list_manager import ListManager


class ContactManager(EntityManager):
    """
    Entity manager for contacts.
    """

    base_path = 'contacts'
    entity_class = Contact
    writable_fields = [
        'attributes',
        'first_name',
        'last_name',
        'lists',
        'email'
    ]
    lookup_field = 'email'

    def normalize_entity(self, entity):
        """
        Fixes the attributes and lists properties - they should not be null.
        Normalizes the lists.

        :param entity Entity
        :return object
        """
        data = super(ContactManager, self).normalize_entity(entity)

        if not type(dict()) == type(data.get('attributes')):
            data['attributes'] = dict()

        list_manager = ListManager(self.api)
        data['lists'] = []
        if isinstance(getattr(entity, 'lists'), type([])):
            for list in entity.lists:
                norm = list_manager.normalize_entity(list)
                norm['hash'] = list.hash
                data['lists'].append(norm)

        return data