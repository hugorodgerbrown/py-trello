""" Contains all Provider classes - used to manage API use

    Classes:
    
    ProviderBase
    BoardProvider
    CardProvider
    ListProvider

"""

from models import Board, Card, List
from trello import client
from exceptions import ResourceUnavailableException
import requests
import json

class ProviderBase():

    """Base class for all entity provider classes.

    The ProviderBase base class holds a reference to the TrelloClient object that actually 
    calls the relevant API. The Provider subclasses contain the URL formatting / logic required
    to drive the API for the relevant entity.

    """

    def __init__(self, trello_client):
        self.client = trello_client


    def get_json(self, path, query_params = {}):

        headers = {'content-type': 'application/json', 'Accept':'application/json'}
        url = self.client.build_url(path)
        try:
            response = requests.get(url, params=query_params, headers=headers)
            if response.status_code != 200:
                raise ResourceUnavailableException(url, response.status_code, response.text)
            else:
                return json.loads(response.text)
        except requests.RequestException:
            # TODO: error checking
            raise

    def post_json(self, path, post_params = {}):

        headers = {'content-type': 'application/json', 'Accept':'application/json'}
        url = self.client.build_url(path)
        try:
            response = requests.post(url, data=post_params, headers=headers)
            return true
        except requests.RequestException:
            # TODO: error checking
            return false

    
class BoardProvider(ProviderBase):

    """ Provider class used to manage the Trello API operations """

    def get_by_id(self, board_id):
        """ Fetches a specific board using the unique id property """
        json_obj = self.get_json('/boards/' + board_id)
        return Board.from_json(json_obj)

    def get_all(self):
        """ Fetches all of the boards that a user has access to """
        json_obj = self.get_json('/members/me/boards/all')
        return Board.from_json_list(json_obj)


class CardProvider(ProviderBase):

    """ Provider class used to manage the Trello API operations """

    def get_by_id(self, card_id):
        """ Fetches a specific Card using the unique id property."""
        json_obj = self.get_json('/cards/'+card_id, query_params = {'badges': False})
        return Card.from_json(json_obj)

    def get_cards(self, list_id):
        """ Fetches all of the Cards on a list"""
        json_obj = self.get_json('/lists/'+list_id+'/cards')
        return Card.from_json_list(json_obj)


class ListProvider(ProviderBase):

    """ Provider class used to access fetch lists from the Trello API """

    def get_by_id(self, list_id):
        """ Fetches a specific List using the unique id property """
        json_obj = self.get_json('/lists/' + list_id)
        return List.from_json(json_obj)

    def get_lists(self, board_id, list_filter = 'all'):
        """ Fetches the lists on a board. """
        json_obj = self.get_json('/boards/'+board_id+'/lists',query_params = {'cards': 'none', 'filter': list_filter})
        return List.from_json_list(json_obj)

    def get_open_lists(self, board_id):
        """ Fetches the open lists on a board. """
        return self.get_lists(board_id, 'open')

    def get_closed_lists(self, board_id):
        """ Fetches the closed lists on a board. """
        return self.get_lists(board_id, 'closed')
