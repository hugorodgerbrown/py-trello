from httplib2 import Http
from urllib import urlencode
from trello import ResourceUnavailable
import json

class Trello(object):

	def __init__(self, api_key, oauth_token):
		"""
		Constructor

		:api_key: API key generated at https://trello.com/1/appKey/generate
		:oauth_token: OAuth token generated by the user
		"""
		self.client = Http()
		self.key = api_key
		self.token = oauth_token

	def logout(self):
		"""Log out of Trello. This method is idempotent."""

		# TODO: refactor
		pass
		#if not self._cookie:
			#return

		#headers = {'Cookie': self._cookie, 'Accept': 'application/json'}
		#response, content = self.client.request(
				#'https://trello.com/logout',
				#'GET',
				#headers = headers,
				#)

		## TODO: error checking
		#self._cookie = None

	def build_url(self, path, query = {}):
		"""
		Builds a Trello URL.

		:path: URL path
		:params: dict of key-value pairs for the query string
		"""
		url = 'https://api.trello.com/1'
		if path[0:1] != '/':
			url += '/'
		url += path
		url += '?'
		url += "key="+self.key
		url += "&token="+self.token

		if len(query) > 0:
			url += "&"+urlencode(query)
		return url

	def list_boards(self):
		"""
		Returns all boards for your Trello user

		:return: a list of Python objects representing the Trello boards. Each board has the 
		following noteworthy attributes:
			- id: the board's identifier
			- name: Name of the board
			- desc: Description of the board
			- closed: Boolean representing whether this board is closed or not
			- url: URL to the board
		"""
		headers = {'Accept': 'application/json'}
		url = self.build_url("/members/me/boards/all")
		response, content = self.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		boards = list()
		for b in json_obj:
			board = Board(self, b['id'])
			board.name = b['name']
			board.description = b['desc']
			board.closed = b['closed']
			board.url = b['url']
			boards.append(board)

		return boards


class Board(object):
	"""Class representing a Trello board. Board attributes are stored as normal Python attributes;
	access to all sub-objects, however, is always an API call (Lists, Cards).
	"""

	def __init__(self, trello, board_id):
		"""Constructor.
		
		:trello: Reference to a Trello object
		:board_id: ID for the board
		"""
		self.trello = trello
		self.id = board_id

	def fetch(self):
		"""Fetch all attributes for this board"""
		headers = {'Accept': 'application/json'}
		url = self.trello.build_url('/boards/'+self.id)
		response, content = self.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		self.name = json_obj['name']
		self.description = json_obj['desc']
		self.closed = json_obj['closed']
		self.url = json_obj['url']
		
	def all_lists(self):
		"""Returns all lists on this board"""
		return self.get_lists('all')

	def open_lists(self):
		"""Returns all open lists on this board"""
		return self.get_lists('open')

	def closed_lists(self):
		"""Returns all closed lists on this board"""
		return self.get_lists('closed')

	def get_lists(self, filter):

		headers = {'Accept': 'application/json'}
		url = self.trello.build_url(
				'/boards/'+self.id+'/lists',
				{'cards': 'none', 'filter': filter})
		response, content = self.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		lists = list()
		for obj in json_obj:
			l = List(self, obj['id'])
			l.name = obj['name']
			l.closed = obj['closed']
			lists.append(l)

		return lists

class List(object):
	"""Class representing a Trello list. List attributes are stored on the object, but access to 
	sub-objects (Cards) require an API call"""

	def __init__(self, board, list_id):
		"""Constructor

		:board: reference to the parent board
		:list_id: ID for this list
		"""
		self.board = board
		self.id = list_id

	def fetch(self):
		"""Fetch all attributes for this list"""
		headers = {'Accept': 'application/json'}
		url = self.board.trello.build_url('/lists/'+self.id)
		response, content = self.board.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		self.name = json_obj['name']
		self.closed = json_obj['closed']
	
	def add_card(self, name, desc = None):
		"""Add a card to this list

		:name: name for the card
		:return: the card
		"""
		headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
		url = self.board.trello.build_url('/lists/'+self.id+'/cards')
		request = {'name': name, 'idList': self.id, 'desc': desc, 'key': self.board.trello.key, 'token': self.board.trello.token}
		response, content = self.board.trello.client.request(
				url,
				'POST',
				headers = headers,
				body = json.dumps(request))

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)

		card = Card(self, json_obj['id'])
		card.name = json_obj['name']
		card.description = json_obj['description']
		card.closed = json_obj['closed']
		card.url = json_obj['url']
		pass

class Card(object):
	""" Class representing a Trello card. Card attributes are stored on the object"""

	def __init__(self, trello_list, card_id):
		"""Constructor

		:trello_list: reference to the parent list
		:card_id: ID for this card
		"""
		self.trello_list = trello_list
		self.id = card_id

	def fetch(self):
		"""Fetch all attributes for this card"""
		headers = {'Accept': 'application/json'}
		url = self.board.trello.build_url('/cards/'+self.id, {'badges': False})
		response, content = self.board.trello.client.request(url, 'GET', headers = headers)

		# error checking
		if response.status != 200:
			raise ResourceUnavailable(url)

		json_obj = json.loads(content)
		self.name = json_obj['name']
		self.description = json_obj['description']
		self.closed = json_obj['closed']
		self.url = json_obj['url']
