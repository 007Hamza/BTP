# -*- coding: utf-8 -*-
# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2012 sakito
# See LICENSE for details.
from __future__ import with_statement

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


class RateLimitStatusTests(unittest.TestCase):

    def setUp(self):
        auth = OAuthHandler(oauth_consumer_key, oauth_consumer_secret)
        auth.set_access_token(oauth_token, oauth_token_secret)
        self.api = API(auth)
        self.api.retry_count = 2
        self.api.retry_delay = 5

    def test_get_header(self):
        self.api.get_header = True
        self.api.rate_limit_status()

    def test_rate_limit_status(self):
        ret = self.api.rate_limit_status()

        self.assertEqual(oauth_token,
                         ret['rate_limit_context']['access_token'])

        res = ret['resources']
        self.assertEqual([
            u'account',
            u'blocks',
            u'users',
            u'friends',
            u'saved_searches',
            u'lists',
            u'search',
            u'application',
            u'trends',
            u'followers',
            u'favorites',
            u'friendships',
            u'geo',
            u'direct_messages',
            u'statuses',
            u'help',
        ], res.keys())

        self.assertEqual(
            15, res['account']['/account/verify_credentials']['limit'])
        self.assertEqual(15, res['account']['/account/settings']['limit'])
        self.assertEqual(15, res['blocks']['/blocks/list']['limit'])
        self.assertEqual(15, res['blocks']['/blocks/ids']['limit'])
        self.assertEqual(180, res['users']['/users/lookup']['limit'])
        self.assertEqual(
            15, res['users']['/users/suggestions/:slug/members']['limit'])
        self.assertEqual(180, res['users']['/users/search']['limit'])
        self.assertEqual(15, res['users']['/users/suggestions/:slug']['limit'])
        self.assertEqual(180, res['users']['/users/show/:id']['limit'])
        self.assertEqual(15, res['users']['/users/suggestions']['limit'])
        self.assertEqual(15, res['users']['/users/contributors']['limit'])
        self.assertEqual(15, res['users']['/users/contributees']['limit'])
        self.assertEqual(15, res['friends']['/friends/ids']['limit'])
        self.assertEqual(
            15, res['saved_searches']['/saved_searches/show/:id']['limit'])
        self.assertEqual(
            15, res['saved_searches']['/saved_searches/list']['limit'])
        self.assertEqual(15, res['lists']['/lists/subscriptions']['limit'])
        self.assertEqual(15, res['lists']['/lists/subscribers/show']['limit'])
        self.assertEqual(15, res['lists']['/lists/statuses']['limit'])
        self.assertEqual(15, res['lists']['/lists/subscribers']['limit'])
        self.assertEqual(15, res['lists']['/lists/list']['limit'])
        self.assertEqual(15, res['lists']['/lists/members/show']['limit'])
        self.assertEqual(15, res['lists']['/lists/show']['limit'])
        self.assertEqual(15, res['lists']['/lists/memberships']['limit'])
        self.assertEqual(15, res['lists']['/lists/members']['limit'])
        self.assertEqual(180, res['search']['/search/tweets']['limit'])
        self.assertEqual(
            180, res['application']['/application/rate_limit_status']['limit'])
        self.assertEqual(15, res['trends']['/trends/available']['limit'])
        self.assertEqual(15, res['trends']['/trends/closest']['limit'])
        self.assertEqual(15, res['trends']['/trends/place']['limit'])
        self.assertEqual(15, res['followers']['/followers/ids']['limit'])
        self.assertEqual(15, res['favorites']['/favorites/list']['limit'])
        self.assertEqual(
            15, res['friendships']['/friendships/outgoing']['limit'])
        self.assertEqual(15, res['friendships']['/friendships/show']['limit'])
        self.assertEqual(
            15, res['friendships']['/friendships/incoming']['limit'])
        self.assertEqual(
            15, res['friendships']['/friendships/lookup']['limit'])
        self.assertEqual(15, res['geo']['/geo/similar_places']['limit'])
        self.assertEqual(15, res['geo']['/geo/id/:place_id']['limit'])
        self.assertEqual(15, res['geo']['/geo/reverse_geocode']['limit'])
        self.assertEqual(15, res['geo']['/geo/search']['limit'])
        self.assertEqual(
            15, res['direct_messages']['/direct_messages/show']['limit'])
        self.assertEqual(
            15, res['direct_messages']['/direct_messages']['limit'])
        self.assertEqual(
            15, res['direct_messages']['/direct_messages/sent']['limit'])
        self.assertEqual(
            180, res['statuses']['/statuses/user_timeline']['limit'])
        self.assertEqual(
            15, res['statuses']['/statuses/mentions_timeline']['limit'])
        self.assertEqual(
            15, res['statuses']['/statuses/home_timeline']['limit'])
        self.assertEqual(180, res['statuses']['/statuses/oembed']['limit'])
        self.assertEqual(180, res['statuses']['/statuses/show/:id']['limit'])
        self.assertEqual(
            15, res['statuses']['/statuses/retweets/:id']['limit'])
        self.assertEqual(15, res['help']['/help/tos']['limit'])
        self.assertEqual(15, res['help']['/help/configuration']['limit'])
        self.assertEqual(15, res['help']['/help/privacy']['limit'])
        self.assertEqual(15, res['help']['/help/languages']['limit'])

    def test_statuses_user_timeline(self):
        ret = self.api.rate_limit_status(resources='statuses')
        self.assertEqual(ret['rate_limit_context']['access_token'],
                         oauth_token)
        self.assertEqual([u'statuses'], ret['resources'].keys())

        ratelimit = ret['resources']['statuses']['/statuses/user_timeline']
        self.assertEqual(180, ratelimit['limit'])

    def test_page_cursor_items(self):
        before_limit = self.api.rate_limit_status(resources='statuses')[
            'resources']['statuses']['/statuses/user_timeline'][
                'remaining']
        items = list(Cursor(self.api.user_timeline).items())
        self.assert_(len(items) > 0)
        after_limit = self.api.rate_limit_status(resources='statuses')[
            'resources']['statuses']['/statuses/user_timeline'][
                'remaining']
        self.assertEqual(3, before_limit - after_limit)

        before_limit = self.api.rate_limit_status(resources='statuses')[
            'resources']['statuses']['/statuses/user_timeline'][
                'remaining']
        items = list(Cursor(self.api.user_timeline, 'twitter').items(30))
        self.assertEqual(30, len(items))
        after_limit = self.api.rate_limit_status(resources='statuses')[
            'resources']['statuses']['/statuses/user_timeline'][
                'remaining']
        self.assertEqual(2, before_limit - after_limit)

    def test_cursor_cursor_items(self):
        before_limit = self.api.rate_limit_status(resources='friends')[
            'resources']['friends']['/friends/ids']['remaining']
        items = list(Cursor(self.api.friends_ids).items())
        self.assertLessEqual(0, len(items))
        after_limit = self.api.rate_limit_status(resources='friends')[
            'resources']['friends']['/friends/ids']['remaining']
        self.assertEqual(1, before_limit - after_limit)

        before_limit = self.api.rate_limit_status(resources='followers')[
            'resources']['followers']['/followers/ids']['remaining']
        items = list(Cursor(self.api.followers_ids, 'twitter').items(30))
        self.assertEquals(30, len(items))
        after_limit = self.api.rate_limit_status(resources='followers')[
            'resources']['followers']['/followers/ids']['remaining']
        self.assertEqual(1, before_limit - after_limit)


if __name__ == '__main__':
    unittest.main()
