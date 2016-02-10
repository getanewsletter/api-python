from entity import Entity


class Contact(Entity):
    """
    Represents a contact object.
    """
    email = None
    attributes = None
    first_name = None
    last_name = None
    lists = None
    url = None
    active = None
    updated = None
    created = None

    def subscribe_to(self, list):
        """
        Subscribes the contact to a list.

        Do not forget to call contact.save()!

        :param list The list to subscribe on.
        """

        if not isinstance(self.lists, type([])):
            self.lists = []
        self.lists.append(list)