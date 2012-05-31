""" This module contains code used to interact with Trello Boards. 

"""
from trello import client, entity

class BoardProvider(entity.EntityProviderBase):

    """ Provider class used to manage the Trello API operations """

    def get_by_id(self, board_id):
        """ Fetches a specific board using the unique id property """
        json_obj = self.client.fetch_json('/boards/' + board_id)
        return Board.from_json(json_obj)

    def get_all(self):
        """ Fetches all of the boards that a user has access to """
        json_obj = self.client.fetch_json('/members/me/boards/all')
        return Board.from_json_list(json_obj)

        
class Board(entity.EntityBase, entity.EntityFactoryBase):

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
