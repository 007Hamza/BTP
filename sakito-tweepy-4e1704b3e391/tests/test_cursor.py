#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

from tweepy2 import (
    API,
    OAuthHandler,
    Cursor,
)

# Configurations
# Must supply twitter account credentials for tests
username = os.environ.get('tweepy_username', '')
password = os.environ.get('tweepy_password', '')
oauth_consumer_key = os.environ.get('tweepy_oauth_consumer_key', '')
oauth_consumer_secret = os.environ.get('tweepy_oauth_consumer_secret', '')
oauth_token = os.environ.get('tweepy_oauth_token', '')
oauth_token_secret = os.environ.get('tweepy_oauth_token_secret', '')

# Unit tests


class TweepyCursorTests(unittest.TestCase):

    def setUp(self):
        auth = OAuthHandler(oauth_consumer_key, oauth_consumer_secret)
        auth.set_access_token(oauth_token, oauth_token_secret)
        self.api = API(auth)
        self.api.retry_count = 2
        self.api.retry_delay = 5

    def test_page_cursor_items(self):
        items = list(Cursor(self.api.user_timeline).items())
        self.assertLessEqual(0, len(items))

        items = list(Cursor(self.api.user_timeline, 'twitter').items(30))
        self.assertEqual(30, len(items))
        for _ in items:
            pass

    def test_page_cursor_pages(self):
        pages = list(Cursor(self.api.user_timeline).pages())
        self.assertLessEqual(0, len(pages))

        pages = list(Cursor(self.api.user_timeline, 'twitter').pages(5))
        self.assertEqual(5, len(pages))
        for _ in pages:
            pass

    def test_page_search_pages(self):
        pages = list(Cursor(self.api.search_tweets, 'twitter').pages(5))
        for _ in pages:
            pass
        pages = list(Cursor(self.api.search_tweets,
                            q='twitter', max_id='271859163712348161').pages(1))
        for _ in pages:
            pass
        pages = list(Cursor(self.api.search_tweets,
                            q='twitter', max_id=None, since_id=None).pages(1))
        for _ in pages:
            pass

    def test_cursor_cursor_items(self):
        items = list(Cursor(self.api.friends_ids).items())
        self.assertLessEqual(0, len(items))

        items = list(Cursor(self.api.followers_ids, 'twitter').items(30))
        self.assertEquals(30, len(items))
        for _ in items:
            pass

    def test_cursor_cursor_pages(self):
        pages = list(Cursor(self.api.friends_ids).pages())
        self.assertLessEqual(0, len(pages))

        pages = list(Cursor(self.api.followers_ids, 'twitter').pages(5))
        self.assertEquals(5, len(pages))
        for _ in pages:
            pass


if __name__ == '__main__':
    unittest.main()
