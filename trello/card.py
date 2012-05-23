""" This module contains code used to interact with Trello Cards. 

"""
from trello import client

class CardProvider(client.EntityProvider):

    """ Provider class used to manage the Trello API operations """

    def get_by_id(self, card_id):
        """ Fetches a specific Card using the unique id property."""
        json_obj = self.client.fetch_json('/cards/'+card_id, query_params = {'badges': False})
        return Card.from_json(json_obj)

    def get_list_cards(self, list_id):
        """ Fetches all of the Cards on a list"""
        json_obj = self.client.fetch_json('/lists/'+list_id+'/cards')
        return Card.from_json_list(json_obj)

class CardFactory(object):

    """ Factory class used to create Card objects from underlying JSON representation """

    @classmethod
    def from_json(cls, json_obj):
        """ Deserializes a Card object from a JSON representation. """
        Card = Card()
        Card.id = json_obj['id']
        Card.name = json_obj['name']
        Card.description = json_obj.get('desc','')
        Card.closed = json_obj['closed']
        Card.url = json_obj['url']
        return Card

    @classmethod
    def from_json_list(cls, json_obj):
        """ Deserializes a collection of Card objects from a JSON representation. """
        cards = list()
        for c in json_obj:
            cards.append(CardFactory.from_json(c))
        return cards

class Card(object):

    """ Class representing a Trello Card entity. """

    def __init__(self):
        pass

    def __str__(self):
        return "(id:%(id)s) %(name)s" % {'name':self.name,'id':self.id}
