""" Contains API models.

    Classes:

    EntityBase
    EntityFactoryBase
    Board
    Card
    List 

"""

class EntityBase():

    """ Base class for all entities - defines common __str__ implementation """

    def __str__(self):
        return "(%(class)s:%(id)s) %(name)s" % {'name':self.name,'id':self.id, 'class':self.__class__.__name__}

    def __repr__(self):
        return '<%(class)s [%(id)s]>' % {'id':self.id, 'class':self.__class__.__name__}


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

       
class Board(EntityBase, EntityFactoryBase):

    """ Class representing a Trello board entity."""

    @classmethod
    def from_json(cls, json_obj):
        """ Deserializes a Board object from a JSON representation. """
        board = Board()
        board.id = json_obj['id']
        board.name = json_obj['name']
        board.description = json_obj.get('desc','')
        board.closed = json_obj['closed']
        board.url = json_obj['url']
        return board


class Card(EntityBase, EntityFactoryBase):

    """ Class representing a Trello Card entity. """

    @classmethod
    def from_json(cls, json_obj):
        """ Deserializes a Card object from a JSON representation. """
        card = Card()
        card.id = json_obj['id']
        card.name = json_obj['name']
        card.description = json_obj.get('desc','')
        card.closed = json_obj['closed']
        card.url = json_obj['url']
        return card


class List(EntityFactoryBase, EntityBase):

    """ Class representing a Trello List entity. """

    @classmethod
    def from_json(cls, json_obj):
        """ Deserializes a List object from a JSON representation. """
        board_list = List()
        board_list.id = json_obj['id']
        board_list.name = json_obj['name']
        board_list.closed = json_obj['closed']
        return board_list
