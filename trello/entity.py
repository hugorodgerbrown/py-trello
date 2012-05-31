""" This module contains core Entity base classes. 

    Classes:

    EntityBase: base class for entity subclasses
    EntityFactoryBase: defines methods used to create entities
    EntityProviderBase: defines methods used to fetch entities

"""

class EntityBase():

    """ Base class for all entities - defines generic __str__ implementation """

    def __str__(self):
        return "(%(class)s:%(id)s) %(name)s" % {'name':self.name,'id':self.id, 'class':self.__class__.__name__}

class EntityFactoryBase():
    
    """ Base class for subclasses that are used to create entity objects from underlying data. """

    @classmethod
    def from_json(cls, json_obj):
        raise NotImplementedError("Subclass \"%s\" does not implement EntityFactoryBase.from_json() method." % str(cls)) # must be overridden by the subclass, otherwise throws exception

    @classmethod
    def from_json_list(cls, json_obj):
        """ Deserializes a collection of objects from a JSON representation. """
        entities = list()
        for entity in json_obj:
            entities.append(cls.from_json(entity))
        return entities


class EntityProviderBase():

    """Base class for all entity provider classes.

    The ProviderBase base class holds a reference to the TrelloClient object that actually 
    calls the relevant API. The Provider subclasses contain the URL formatting / logic required
    to drive the API for the relevant entity.

    """

    def __init__(self, trello_client):
        self.client = trello_client
