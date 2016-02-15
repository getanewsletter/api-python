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

    @staticmethod
    def hash_in_contacts_lists(hash, list):

        if any(sub['hash'] == hash for sub in list):
            return True
        return False

    def subscribe_to(self, list):
        """
        Subscribes the contact to a list.

        Do not forget to call contact.save()!

        :param list The list to subscribe on.
        """

        if not isinstance(self.lists, type([])):
            self.lists = []

        if not self.hash_in_contacts_lists(list.hash, self.lists):
            # Will not activate already cancelled subscription
            # only put it back in listing.
            self.lists.append(list)

    def unsubscribe_from(self, list):
        """
        Unsubscribes the contact from a list.
        This cancels the subscription but does not remove the list from the contact.

        Do not forget to call contact.save()!

        :param list The List to unsubscribe from.
        """
        if not isinstance(self.lists, type([])):
            self.lists = []

        if self.hash_in_contacts_lists(list.hash, self.lists):
            for i in (i for i, v in enumerate(self.lists) if v['hash'] == list.hash):
                self.lists[i]['cancelled'] = True

    def delete_subscription_from(self, list):
        """
        Deletes contact from list.
        This will remove the user from the list.

        Do not forget to call contact.save()!

        :param list: The List to delete contact from.
        """
        if self.hash_in_contacts_lists(list.hash, self.lists):
            for i in (i for i, v in enumerate(self.lists) if v['hash'] == list.hash):
                self.lists.remove(self.lists[i])


