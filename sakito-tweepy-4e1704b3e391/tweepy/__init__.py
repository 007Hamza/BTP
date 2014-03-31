# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

"""
Tweepy Twitter API library
"""
API_VERSION = '1'
__version__ = '1.11proxy4'
__author__ = 'Joshua Roesslein'
__license__ = 'MIT'

from tweepy.models import (
    Status,
    User,
    DirectMessage,
    Friendship,
    SavedSearch,
    SearchResult,
    ModelFactory
)
from tweepy.error import TweepError
from tweepy.api import API
from tweepy.cache import Cache, MemoryCache, FileCache
from tweepy.auth import OAuthHandler
from tweepy.streaming import Stream, StreamListener
from tweepy.cursor import Cursor


def debug(enable=True, level=1):

    import httplib
    httplib.HTTPConnection.debuglevel = level
