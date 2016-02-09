ganapi
=======

The ganapi library presents a simple and easy to use interface to the Get a Newsletter's REST API.

Requirements
------------
* Python 2.7.6 tested
* requests 2.2.1
* httmock for tests

Installation
------------
Via PIP pip install ganapi


Usage
-----
Start by creating an instance of the ```Api``` object:
```python
from ganapi import Api

token = '...'
gan = Api(token)
```
Here ```token``` variable must contain a valid [API token](http://help.getanewsletter.com/en/support/api-token-2/) string.

#### The contact object
The instances of the Contact class represent the contact entities in the API.
They have the following fields:

*Required fields*
* ```email``` - contact's email. It's also a ***_lookup field_*** - required when updating or deleting the contact.

*Optional fields*
* ```attributes``` - list of the contact's [attributes](http://help.getanewsletter.com/en/support/attribute-overview/).
* ```first_name```
* ```last_name```
* ```lists``` - list of the newsletters for which this contact is subscribed to.

*Read-only fields*
* ```url``` - the contact's resource URL.
* ```active``` - true if the contact is active and can receive mails, false otherwise.
* ```updated``` - the date of the last change.
* ```created``` - the date of creation.

#### Retreiving a contact
You have to create an instance of the ```ContactManager``` class and then use it's ```get()``` method to retrieve the contact you need.
```python
from ganapi import ContactManager

contact_manager = ContactManager(gan)
contact = contact_manager.get('john.doe@example.com')
```
The manager methods will throw an ```RequestException``` in case of HTTP error from the API, so it's a good idea to catch it.
```python

try:
    contact = contact_manager.get('john.doe@example.com')
except RequestException as e:
    if e.response.code == 404:
        print 'Contact not found!'
    else:
        print 'API error: ' + e


```

#### Creating a contact
```python

contact = Contact()
contact.email = 'jane.doe@example.com'
contact.first_name = 'Jane'

contact_manager.save(contact)
```
This will create a new contact and save it. Again, it'll be a good idea to catch exceptions when calling the ```save()``` method. The API will respond with an error if the contact already exists.
One way to avoid it is to force the creation of the contact, overwriting the existing one:
```python

contact_manager.overwrite(contact)
```

Both ```save()``` and ```overwrite()``` will return the same contact object with it's read-only fields updated (e.g. ```created```, ```updated```).

```python

contact = contact_manager.save(contact)
print contact.created
```

#### Updating an existing contact
```python

# Get the contact.
contact = contact_manager.get('john.doe@example.com')
# Change some fields.
contact.first_name = 'John'
# Save it.
contact_manager.save(contact)
```
You can avoid making two calls to the API by forcing a *partial update*.
```python

contact = Contact()
contact.set_persisted()
contact.email = 'john.doe@example.com'
contact.first_name = 'John'
contactManager.save(contact)
```
Calling ```set_persisted()``` on the contact object marks it like it's already existing and coming from the API. The calls to the ```save()``` method when a contact is maked as existing will do only a *partial update*, i.e. update only the supplied fields and skipping all the ```None``` fields.
Do not forget that ```email``` is a ***_lookup field_*** and required when updating or deleting the contact.

#### Deleting a contact
```python

contact_manager.delete(contact)
```

#### The list object
The instances of the List class represent the [lists](http://help.getanewsletter.com/en/support/lists-overview/) in the API. They have the following structure:

*Required fields*
* ```email``` - sender's email.
* ```name``` - name of the list.
* ```sender``` - sender's name.
*
*Optional fields*
* ```description```

*Lookup field*
* ```hash``` - the list's unique hash.

*Read-only fields*
* ```responders_count```
* ```subcribers```
* ```created```
* ```url```
* ```subscribers_count```
* ```active_subscribers_count```
* ```responders```

#### Retreiving, creating, updating and deleting a list
The CRUD operations on lists are no different from the operations on contacts:
```python

list_manager = ListManager(gan)

# Retrieve a list.
list = list_manager.get('hash')

# Update the list.
list.name = 'my list'
list = list_manager.save(list)
print list.updated

# Create new list.
new_list = List()
new_list.email = 'john.doe@example.com' # required fields
new_list.name = 'my new list'
new_list.sender = 'John Doe'
list_manager.save(new_list)

# Partial update.
list = List()
list.hash = 'hash' # lookup field
list.name = 'updated list'
list_manager.save(list)

# Delete the list.
list_manager.delete(list)

```

#### Subscribing a contact to a list
```python

contact.subscribe_to(list)
contact_manager.save(contact)
```
You can also create a new contact automatically subscribed.
```python

contact = new Contact()
contact.email = 'john.doe@example.com'
contact.subscribe_to(list)
contact_manager.save(contact)
```
