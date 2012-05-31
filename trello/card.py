""" This module contains code used to interact with Trello Cards. 

    This module separates out the Factory implementation to a separate class.

"""
from trello import entity

class CardProvider(entity.EntityProviderBase):

    """ Provider class used to manage the Trello API operations """

    def get_by_id(self, card_id):
        """ Fetches a specific Card using the unique id property."""
        json_obj = self.fetch_json('/cards/'+card_id, query_params = {'badges': False})
        return CardFactory.from_json(json_obj)

    def get_cards(self, list_id):
        """ Fetches all of the Cards on a list"""
        json_obj = self.fetch_json('/lists/'+list_id+'/cards')
        return CardFactory.from_json_list(json_obj)


class CardFactory(entity.EntityFactoryBase):

    """ Factory class used to create Card objects from underlying JSON representation """

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


class Card(entity.EntityBase):
    """ Class representing a Trello Card entity. """
