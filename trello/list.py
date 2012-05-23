""" This module contains code used to interact with Trello Lists. 

"""
from trello import client

class ListProvider(client.EntityProvider):

    """ Provider class used to access fetch lists from the Trello API """

    def get_by_id(self, list_id):
        """ Fetches a specific List using the unique id property """
        json_obj = self.client.fetch_json('/lists/' + list_id)
        return ListFactory.from_json(json_obj)

    def get_lists(self, board_id, list_filter = 'all'):
        """ Fetches the lists on a board. """
        json_obj = self.client.fetch_json('/boards/'+board_id+'/lists',query_params = {'cards': 'none', 'filter': list_filter})
        return ListFactory.from_json_list(json_obj)

    def get_open_lists(self, board_id):
        """ Fetches the open lists on a board. """
        return self.get_lists(board_id, 'open')

    def get_closed_lists(self, board_id):
        """ Fetches the closed lists on a board. """
        return self.get_lists(board_id, 'closed')

class ListFactory(object):

    """ Factory class used to create List objects from underlying JSON representation """

    @classmethod
    def from_json(cls, json_obj):
        """ Deserializes a List object from a JSON representation. """
        board_list = List()
        board_list.id = json_obj['id']
        board_list.name = json_obj['name']
        board_list.closed = json_obj['closed']
        return board_list

    @classmethod
    def from_json_list(cls, json_obj):
        """ Deserializes a collection of List objects from a JSON representation. """
        lists = list()
        for l in json_obj:
            lists.append(ListFactory.from_json(l))
        return lists

class List(object):

    """ Class representing a Trello List entity. """

    def __init__(self):
        pass

    def __str__(self):
        return "(list:%(id)s) %(name)s" % {'name':self.name,'id':self.id}


