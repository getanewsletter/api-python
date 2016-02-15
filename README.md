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
Via PIP:
```bash
pip install ganapi
```

Usage
-----
Start by creating an instance of the ```Api``` object:
```python
from ganapi import Api

token = '...'
gan_api = Api(token)
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

contact_manager = ContactManager(gan_api)
contact = contact_manager.get('john.doe@example.com')
```
The manager methods will throw an ```HTTPError``` in case of HTTP error from the API, so it's a good idea to catch it.
```python

try:
    contact = contact_manager.get('john.doe@example.com')
except HTTPError as e:
    if e.response.code == 404:
        print 'Contact not found!'
    else:
        print 'API error: ' + e


```

### Querying for contacts
You have to create an instance of the ```ContactManager``` class and then use it's ```query()``` method to retrieve the contacts you need.
```query()``` takes a dict of [url parameters](https://api.getanewsletter.com/v3/docs/contacts/#get-contacts)  and will return a ```PaginatedResultSet``` with the first page of contacts in a list in PaginatedResultSet.entities.

```python
# Get PaginatedResultSet containing contacts with emails starting with name@.
queried_contacts = contact_manager.query({'search_email': 'name@'})

# list of contacts in current page(1)
queried_contacts.entities

# list of contacts in next page(2) if available and update PaginatedResultSet
queried_contacts.next()

# list of contacts in previous page(1) if available and update PaginatedResultSet
queried_contacts.prev()


```

#### Creating a contact
```python

contact = contact_manager.create()
contact.email = 'jane.doe@example.com'
contact.first_name = 'Jane'

contact.save()
```
This will create a new contact and save it. Again, it'll be a good idea to catch exceptions when calling the ```save()``` method. The API will respond with an error if the contact already exists.
One way to avoid it is to force the creation of the contact, overwriting the existing one:
```python

contact.overwrite()
```

Both ```save()``` and ```overwrite()``` will return the same contact object with it's read-only fields updated (e.g. ```created```, ```updated```).

```python

contact = contact.save()
print contact.created
```

#### Updating an existing contact
```python

# Get the contact.
contact = contact_manager.get('john.doe@example.com')
# Change some fields.
contact.first_name = 'John'
# Save it.
contact.save()
```
You can avoid making two calls to the API by forcing a *partial update*.
```python

contact = contact_manager.create()
contact.set_persisted()
contact.email = 'john.doe@example.com'
contact.first_name = 'John'
contact.save()
```
Calling ```set_persisted()``` on the contact object marks it like it's already existing and coming from the API. The calls to the ```save()``` method when a contact is maked as existing will do only a *partial update*, i.e. update only the supplied fields and skipping all the ```None``` fields.
Do not forget that ```email``` is a ***_lookup field_*** and required when updating or deleting the contact.

#### Deleting a contact
```python

contact.delete()
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

list_manager = ListManager(gan_api)

# Retrieve a list.
list = list_manager.get('hash')

# Update the list.
list.name = 'my list'
list = list.save()
print list.updated

# Create new list.
new_list = list_manager.create()
new_list.email = 'john.doe@example.com' # required fields
new_list.name = 'my new list'
new_list.sender = 'John Doe'
new_list.save()

# Partial update.
list = list_manager.create()
list.hash = 'hash' # lookup field
list.name = 'updated list'
list.save()

# Delete the list.
list.delete()

```

#### Subscribing a contact to a list
```python

contact.subscribe_to(list)
contact.save()
```
You can also create a new contact automatically subscribed.
```python

contact = contact_manager.create()
contact.email = 'john.doe@example.com'
contact.subscribe_to(list)
contact.save()
```
#### Unsubscribing a contact from a list
```python

contact.unsubscribe_from(list)
contact.save()
```
#### Deleting a contacts subscription from a list
```python

contact.delete_subscription_from(list)
contact.save()
```

#### The attribute object
The instances of the Attribute class represent the attribute entities in the API.
They have the following fields:

*Required fields*
* ```name``` - attribute name.

*Lookup field*
* ```code``` - the slugified attribute code. required when updating or deleting the attribute. *The name "A new attribute" code will be "a-new-attribute"*

*Read-only fields*
* ```url``` - the attribute resource URL.
* ```usage_count``` - number of usages.


#### Retreiving an attribute
You have to create an instance of the ```AttributeManager``` class and then use it's ```get()``` method to retrieve the attribute you need.
```python
from ganapi import AttributeManager

attribute_manager = AttributeManager(gan_api)
attribute = attribute_manager.get('code')
```
The manager methods will raise a ```HTTPError``` in case of HTTP error from the API, so it's a good idea to catch it.
```python

try:
    attribute = attribute_manager.get('code')
except HttpError as e:
    if e.response.code == 404:
        print 'Attribute not found!'
    else:
        print 'API error: ' + e


```

#### Creating an attribute
```python

attribute = attribute_manager.create()
attribute.name = 'City'

attribute.save()
```
This will create a new attribute and save it. Again, it'll be a good idea to catch exceptions when calling the ```save()``` method. The API will respond with an error if the attribute already exists.
One way to avoid it is to force the creation of the attribute, overwriting the existing one:
```python

attribute.overwrite()
```

Both ```save()``` and ```overwrite()``` will return the same attribute object with it's read-only fields updated (e.g. ```url```, ```usage_count```).

```python

attribute = attribute.save()
print attribute.usage_count
```

#### Updating an existing attribute
```python

# Get the attribute.
attribute = attribute_manager.get('code')
# Change name field.
attribute.name = 'Changed!'
# Save it.
attribute.save()
```
You can avoid making two calls to the API by forcing a *partial update*.
```python

attribute = attribute_manager.create()
attribute.set_persisted()
attribute.code = 'code'
attribute.name = 'Changed!'
attribute.save()
```
Calling ```set_persisted()``` on the attribute object marks it like it's already existing and coming from the API. The calls to the ```save()``` method when a attribute is made as existing will do only a *partial update*, i.e. update only the supplied fields and skipping all the ```None``` fields.
Do not forget that ```code``` is a ***_lookup field_*** and required when updating or deleting the attribute.

#### Deleting an attribute
```python

attribute.delete()
```

### Get all entities of type
You can get all contacts, lists or attributes in a generator using the ```all()``` method on their manager.

*Parameters*
* ```start``` - start index (default: 0)
* ```stop``` stop index (default: float('inf'))


```python
# Print all contacts emails
all_contacts = contact_manager.all()
for contact in all_contacts:
    print contact.email
    

# Get a generator starting on contact 100 stopping on contact 200
all_contacts = contact_manager.all(start=100, stop=200)

```



#### The PaginatedResultSet class
The instance of the PaginatedResultSet class represent the result of get from the API.

*Parameters*
* ```data``` - json of result from the ```query()``` method in the managers.
* ```manager``` - the manager using ```query()```.

*Properties*
* ```next_link``` - URL to get the next page of the results.
* ```previous_link``` - URL to get the previous page of the results.
* ```manager``` - ```EntityManager``` currently used.
* ```entities``` - List of ```Entity``` for the current result page.
* ```count``` - Total amount of entity results in all pages.

*Methods*
* ```prev()``` - replaces the instance with results from the previous page and returns entities.
* ```next()``` - replaces the instance with results from the next page and returns entities.

```next()``` and ```prev()``` will raise ```StopIteration``` if the end of the direction has been reached.
They will raise ```HTTPError``` in case of HTTP error from the API,