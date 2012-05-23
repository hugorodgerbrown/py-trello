""" This module contains code used to interact with Trello Boards. 

"""
from trello import client

class BoardProvider(client.EntityProvider):

    """ Provider class used to manage the Trello API operations """

    def get_by_id(self, board_id):
        """ Fetches a specific board using the unique id property """
        json_obj = self.client.fetch_json('/boards/' + board_id)
        return BoardFactory.from_json(json_obj)

    def get_all(self):
        """ Fetches all of the boards that a user has access to """
        json_obj = self.client.fetch_json('/members/me/boards/all')
        return BoardFactory.from_json_list(json_obj)

class BoardFactory(object):

    """ Factory class used to create Board objects from underlying JSON representation """

    def __init__(self):
        pass

    def __str__(self):
        return "(id:%(id)s) %(name)s" % {'name':self.name,'id':self.id}

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

    @classmethod
    def from_json_list(cls, json_obj):
        """ Deserializes a collection of Board objects from a JSON representation. """
        boards = list()
        for b in json_obj:
            boards.append(BoardFactory.from_json(b))
        return boards

class Board(object):

    """ Class representing a Trello board entity.

        Board objects can be created from a JSON representation using the BoardFactory class.
    """

    def __init__(self):
        pass

    def __str__(self):
        return "(board:%(id)s) %(name)s" % {'name':self.name,'id':self.id}
