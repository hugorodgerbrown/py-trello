Python wrapper around the Trello API used to experiment with Python programming patterns (there are other Trello API clients available). It's a "(retired) .net developer takes on python" experiment - so please bear that in mind when looking at it.

This project was forked from https://github.com/sarumont/py-trello and has been updated to in an attempt to simplify it (or unsimplify, depending on your point of view). All (constructive) feedback is welcome.

_At the moment I have only implemented some GET operations on Board, List and Card entities. It covers about 10% of the total Trello API. Do not use this if you are looking for a comprehensive solution._

The core of the solution is based around three concepts:

* entities, which contain data and represent API resources
* providers, which manage API interaction, and
* factories, which manage the creation of entities from the API response JSON

The Provider class is where you will find all of the entity retrieval methods - get_all, get_by_id, get_by_x etc. In concrete terms the provider is responsible formatting the API URLs, determining which API to call, and for converting the output back to the relevant Entity. It does this using a Factory class.

I have used python's multiple inheritance to incorporate both entity and factory classes into a single subclass for each entity type (Board, List, Card etc.) I started out having two classes - entity and entity factory, and then decided to combine them into one. Not entirely sure if this works or not, but the result is pretty clean.

The other main class provided by this project is the TrelloClient, which is the main class with which users of the library will interact. The TrelloClient class contains the logic for interacting with the API itself - managing the HTTP calls formatting URLs, API tokens etc. This class is essentially unchanged from the original, so h/t to Richard Kolkovich (sarumont) that. Thank you Richard.

Using this approach, the work required to add a new entity is as follows (using Widget as the example):

* Create the Widget class, inheriting from both EntityBase and EntityFactoryBase classes
* Implement the Widget.from_json method
* Create the WidgetProvider class
* Implement any relevant get_xxxx methods required

Sample usage of the client library is as follows:

``` python
from trello.client import TrelloClient
from trello.board import Board, BoardProvider

TRELLO_API_KEY = 'YOUR_KEY_GOES_HERE'
TRELLO_TOKEN = 'YOUR_TOKEN_GOES_HERE'

client = TrelloClient(TRELLO_API_KEY, TRELLO_TOKEN)
boards = BoardProvider(client)

# fetch a single board object, using its unique id
my_first_board = boards.get_by_id(board_id)

# fetch all of the boards the current user has access to
all_my_boards = boards.get_all()
for b in all_my_boards:
    print b.name
```

### Questions / alternative approaches

All comments / feedback welcome - this is a learning exercise.

### Running the tests

I have put a single test in - it calls the API to recursively GET all of your boards, lists and cards, and print them out to the console. 

In order to run the tests:

* Replace the TRELLO_TOKEN and TRELLO_API_KEY with your own values from https://trello.com/1/appKey/generate
* Run (from py-trello/):

```
PYTHONPATH=. python test/test_trello.py
```