from trello.models import Board, Card, List
from trello.providers import BoardProvider, ListProvider, CardProvider
from trello.client import TrelloClient
import unittest

# get your token / key from here - https://trello.com/1/appKey/generate
TRELLO_API_KEY = ''
TRELLO_TOKEN = ''

class TrelloClientTestCase(unittest.TestCase):

    """
    Tests for TrelloClient API. Note these test are in order to preserve dependencies, as an API 
    integration cannot be tested independently.
    """

    def setUp(self):
        self.client = TrelloClient(TRELLO_API_KEY, TRELLO_TOKEN)
        self.boards = BoardProvider(self.client)
        self.lists = ListProvider(self.client)
        self.cards = CardProvider(self.client)

    def tearDown(self): 
        #self._trello.logout()
        pass

    def test_recurse(self):
        """ Gets all boards and all lists on those boards """
        print 'Recursively seeking all boards, lists and cards available to this user'
        for b in self.boards.get_all():
            print b
            # now loop through the lists
            for l in self.lists.get_lists(b.id):
                print "  %s" % l
                # now loop through the lists
                for c in self.cards.get_cards(l.id):
                    print "    %s" % c


if __name__ == "__main__":
#    TRELLO_TOKEN = '123'
    unittest.main()
