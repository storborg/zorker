Zorker - A Twitter bot to play text adventure games
===================================================

`Scott Torborg <http://www.scotttorborg.com>`_


Installation
============

Install with pip::

    $ pip install zorker


Running
=======

First set up a new Twitter app, noting consumer key (API key), consumer secret (API secret), access token, and access token secret. There are `helpful instructions for this here <http://nodotcom.org/python-twitter-tutorial.html>`_.

Create a config file, something like ``zorker.ini``::

    [zorker]
    consumer_key = ...
    consumer_secret = ...
    access_token = ...
    access_token_secret = ...
    screen_name = zorker
    game_file = zork1.z5

Run the bot::

    $ zorker zorker.ini


License
=======

Zorker is licensed under an MIT license. Please see the LICENSE file for more
information.
