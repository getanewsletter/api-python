import unittest
from ganapi.entity import Entity


class EntityTest(unittest.TestCase):
    def test_persisted(self):
        new_entity = Entity({'test'})
        self.assertFalse(new_entity.is_persisted())

        _new_entity = new_entity.set_persisted()
        self.assertEqual(_new_entity, new_entity)
        self.assertTrue(new_entity.is_persisted())

        new_entity.set_persisted(False)
        self.assertFalse(new_entity.is_persisted())