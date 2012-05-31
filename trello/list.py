""" This module contains code used to interact with Trello Lists. 

    This module uses multiple inheritance to incorporate both
    EntityFactoryBase and EntityBase into the List class. It's
    a combination of the approaches used in the Board and Card classes.

"""
from trello import client, entity

class ListProvider(entity.EntityProviderBase):

    """ Provider class used to access fetch lists from the Trello API """

    def get_by_id(self, list_id):
        """ Fetches a specific List using the unique id property """
        json_obj = self.client.fetch_json('/lists/' + list_id)
        return List.from_json(json_obj)

    def get_lists(self, board_id, list_filter = 'all'):
        """ Fetches the lists on a board. """
        json_obj = self.client.fetch_json('/boards/'+board_id+'/lists',query_params = {'cards': 'none', 'filter': list_filter})
        return List.from_json_list(json_obj)

    def get_open_lists(self, board_id):
        """ Fetches the open lists on a board. """
        return self.get_lists(board_id, 'open')

    def get_closed_lists(self, board_id):
        """ Fetches the closed lists on a board. """
        return self.get_lists(board_id, 'closed')

class List(entity.EntityFactoryBase, entity.EntityBase):

    """ Class representing a Trello List entity. """

    @classmethod
    def from_json(cls, json_obj):
        """ Deserializes a List object from a JSON representation. """
        board_list = List()
        board_list.id = json_obj['id']
        board_list.name = json_obj['name']
        board_list.closed = json_obj['closed']
        return board_list


