class Entity():

    def __init__(self, manager):
        self.manager = manager
    """
     Flag showing that the entity exists or not in the storage.
    :var bool
    """
    _persisted = False

    def is_persisted(self):
        """
        Returns the persisted status of the entity, whether it exists
        in the storage or not.

        :returns: boolean
        """
        return self._persisted

    def set_persisted(self, persisted=True):
        """
        Sets the persisted status of the entity.
        Except in special cases, normally you should not use this method.
        You may call set_persisted() on an entity in order to make
        partial update on save().

        :param persisted (optional) The new persisted status. True by default.
        """
        self._persisted = persisted
        return self

    def save(self, overwrite=False):
        return self.manager.save(self, overwrite)

    def overwrite(self):
        return self.save(overwrite=True)

    def delete(self):
        return self.manager.delete(self)