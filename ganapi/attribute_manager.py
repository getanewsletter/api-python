from attribute import Attribute
from entity_manager import EntityManager


class AttributeManager(EntityManager):
    """
    Entity manager for contacts.
    """

    base_path = 'attributes'
    entity_class = Attribute
    writable_fields = [
        'name',
    ]
    lookup_field = 'code'
