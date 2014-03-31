# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

"""
Tweepy Twitter API library
"""
VERSION = (2, 0, 8, 'final', 0)
API_VERSION = '1.1'
__author__ = 'Joshua Roesslein'
__license__ = 'MIT'

from tweepy2.models import (
    Status,
    User,
    DirectMessage,
    Friendship,
    SavedSearch,
    SearchResult,
    ModelFactory
)
from tweepy2.error import TweepError
from tweepy2.api import API
from tweepy2.cache import Cache, MemoryCache, FileCache
from tweepy2.auth import OAuthHandler
from tweepy2.streaming import Stream, StreamListener
from tweepy2.cursor import Cursor
from tweepy2 import version

__version__ = version.get_version()


def debug(enable=True, level=1):

    import httplib
    httplib.HTTPConnection.debuglevel = level
