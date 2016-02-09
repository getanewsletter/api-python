from entity_manager import EntityManager
from list import List


class ListManager(EntityManager):
    """
    Entity manager for the List entity.
    """
    base_path = 'lists'
    entity_class = List
    writable_fields = [
        'email',
        'name',
        'sender',
        'description'
    ]
    lookup_field = 'hash'