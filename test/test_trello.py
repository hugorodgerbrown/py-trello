#from trello import TrelloClient
from trello.board import Board, BoardProvider
from trello.card import Card, CardProvider
from trello.list import List, ListProvider
from trello.client import TrelloClient
import unittest
import os
import sys

TRELLO_API_KEY = 'f1cb356eec7ce49e5479615a0e5c5357'
TRELLO_TOKEN = 'bc49e6f1e6b0302a5edf0a01c91cf39e56604a90a70472878129cb527d79cb2d'

class TrelloClientTestCase(unittest.TestCase):

    """
    Tests for TrelloClient API. Note these test are in order to preserve dependencies, as an API 
    integration cannot be tested independently.
    """

    def setUp(self):
        self.client = TrelloClient(TRELLO_API_KEY, TRELLO_TOKEN)
        self.boards = BoardProvider(self.client)
        self.cards = CardProvider(self.client)
        self.lists = ListProvider(self.client)

    def tearDown(self): 
        #self._trello.logout()
        pass

#   def test001_get_board_by_id(self):
#       board = self.boards.get_by_id('4fbcbe42608cb6817410987e')
#       print board

#   def test002_get_all_boards(self):
#           len(self.boards.get_all()),
#           int(os.environ['TRELLO_TEST_BOARD_COUNT']))

    def test_recurse(self):
        """ Gets all boards, all lists on those boards, and then all cards on those lists. """
        print 'Recursively seeking all boards, lists and cards available to this user'
        for b in self.boards.get_all():
            print b
            # now loop through the lists
            for l in self.lists.get_lists(b.id):
                print "  %s" % l
                # and finally, loop through the cards
                for c in self.cards.get_cards(l.id):
                    print "    %s" % c
"""
    def test002_get_all_boards(self):
        boards = self._boardProvider.get_all()
        for b in boards:
            print str(b)

    def test01_list_boards(self):
        self.assertEquals(
                len(self._trello.list_boards()),
                int(os.environ['TRELLO_TEST_BOARD_COUNT']))

    def test10_board_attrs(self):
        boards = self._trello.list_boards()
        for b in boards:
            self.assertIsNotNone(b.id, msg="id not provided")
            self.assertIsNotNone(b.name, msg="name not provided")
            self.assertIsNotNone(b.description, msg="description not provided")
            self.assertIsNotNone(b.closed, msg="closed not provided")
            self.assertIsNotNone(b.url, msg="url not provided")

    def test20_board_all_lists(self):
        boards = self._trello.list_boards()
        for b in boards:
            try:
                b.all_lists()
            except Exception as e:
                self.fail("Caught Exception getting lists")

    def test21_board_open_lists(self):
        boards = self._trello.list_boards()
        for b in boards:
            try:
                b.open_lists()
            except Exception as e:
                self.fail("Caught Exception getting open lists")

    def test22_board_closed_lists(self):
        boards = self._trello.list_boards()
        for b in boards:
            try:
                b.closed_lists()
            except Exception as e:
                self.fail("Caught Exception getting closed lists")

    def test30_list_attrs(self):
        boards = self._trello.list_boards()
        for b in boards:
            for l in b.all_lists():
                self.assertIsNotNone(l.id, msg="id not provided")
                self.assertIsNotNone(l.name, msg="name not provided")
                self.assertIsNotNone(l.closed, msg="closed not provided")
            break # only need to test one board's lists
    
    def test40_list_cards(self):
        boards = self._trello.list_boards()
        for b in boards:
            for l in b.all_lists():
                for c in l.list_cards():
                    self.assertIsNotNone(c.id, msg="id not provided")
                    self.assertIsNotNone(c.name, msg="name not provided")
                    self.assertIsNotNone(c.description, msg="description not provided")
                    self.assertIsNotNone(c.closed, msg="closed not provided")
                    self.assertIsNotNone(c.url, msg="url not provided")
                break
            break
        pass

    def test50_add_card(self):
        boards = self._trello.list_boards()
        board_id = None
        for b in boards:
            if b.name != os.environ['TRELLO_TEST_BOARD_NAME']:
                continue

            for l in b.open_lists():
                try:
                    name = "Testing from Python - no desc"
                    card = l.add_card(name)
                except Exception as e:
                    print str(e)
                    self.fail("Caught Exception adding card")

                self.assertIsNotNone(card, msg="card is None")
                self.assertIsNotNone(card.id, msg="id not provided")
                self.assertEquals(card.name, name)
                self.assertIsNotNone(card.closed, msg="closed not provided")
                self.assertIsNotNone(card.url, msg="url not provided")
                break
            break
        if not card:
            self.fail("No card created")

    def test51_add_card(self):
        boards = self._trello.list_boards()
        board_id = None
        for b in boards:
            if b.name != os.environ['TRELLO_TEST_BOARD_NAME']:
                continue

            for l in b.open_lists():
                try:
                    name = "Testing from Python"
                    description = "Description goes here"
                    card = l.add_card(name, description)
                except Exception as e:
                    print str(e)
                    self.fail("Caught Exception adding card")

                self.assertIsNotNone(card, msg="card is None")
                self.assertIsNotNone(card.id, msg="id not provided")
                self.assertEquals(card.name, name)
                self.assertEquals(card.description, description)
                self.assertIsNotNone(card.closed, msg="closed not provided")
                self.assertIsNotNone(card.url, msg="url not provided")
                break
            break
        if not card:
            self.fail("No card created")

def suite():
    tests = ['test01_list_boards', 'test10_board_attrs', 'test20_add_card']
    return unittest.TestSuite(map(TrelloClientTestCase, tests))
"""

if __name__ == "__main__":
#    if (len(sys.argv) < 2):
#        print "Usage: test_trello.py <api_key> <token>"
#        sys.exit()
#    TRELLO_API_KEY = str(sys.argv[0])
#    TRELLO_TOKEN = sys.argv[1]
    unittest.main()
