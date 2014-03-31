#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import random

from tweepy2 import (
    API,
    OAuthHandler,
    Friendship,
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


class TweepyAPITests(unittest.TestCase):

    def setUp(self):
        auth = OAuthHandler(oauth_consumer_key, oauth_consumer_secret)
        auth.set_access_token(oauth_token, oauth_token_secret)
        self.api = API(auth)
        self.api.retry_count = 2
        self.api.retry_delay = 5

    def test_mentions_timeline(self):
        self.api.mentions_timeline()

    def test_user_timeline(self):
        self.api.user_timeline()
        self.api.user_timeline('twitter')

    def test_home_timeline(self):
        self.api.home_timeline()

    def test_retweets_of_me(self):
        self.api.retweets_of_me()

    @unittest.skip('TODO')
    def test_retweets(self):
        self.api.retweets(123)

    def test_get_status(self):
        self.api.get_status(id=123)

    def test_update_and_destroy_status(self):
        # test update
        text = 'testing %i' % random.randint(0, 1000)
        update = self.api.update_status(status=text)
        self.assertEqual(update.text, text)

        # test destroy
        deleted = self.api.destroy_status(id=update.id)
        self.assertEqual(deleted.id, update.id)

    @unittest.skip('PAUSE')
    def test_retweet(self):
        s = self.api.retweet(123)
        s.destroy()

    @unittest.skip('PAUSE')
    def test_update_with_media(self):
        self.api.update_with_media()

    def test_oembed(self):
        self.api.oembed(id=123)

    def test_search_tweets(self):
        self.api.search_tweets('tweepy')

    def test_direct_messages(self):
        self.api.direct_messages()

    def test_sent_direct_messages(self):
        self.api.sent_direct_messages()

    def test_send_and_destroy_direct_message(self):
        # send
        sent_dm = self.api.send_direct_message(username, text='test message')
        self.assertEqual(sent_dm.text, 'test message')
        self.assertEqual(sent_dm.sender.screen_name, username)
        self.assertEqual(sent_dm.recipient.screen_name, username)

        # show
        self.api.get_direct_message(sent_dm.id)

        # destroy
        destroyed_dm = self.api.destroy_direct_message(sent_dm.id)
        self.assertEqual(destroyed_dm.text, sent_dm.text)
        self.assertEqual(destroyed_dm.id, sent_dm.id)
        self.assertEqual(destroyed_dm.sender.screen_name, username)
        self.assertEqual(destroyed_dm.recipient.screen_name, username)

    def test_friends_ids(self):
        self.api.friends_ids(username)

    def test_followers_ids(self):
        self.api.followers_ids(username)

    def test_lookup_friendships(self):
        self.api.lookup_friendships(screen_names=['episod', 'twitterapi'])

    def test_friendships_incoming(self):
        self.api.friendships_incoming()

    def test_friendships_outgoing(self):
        self.api.friendships_outgoing()

    def test_create_destroy_friendship(self):
        enemy = self.api.destroy_friendship('twitter')
        self.assertEqual(enemy.screen_name, 'twitter')

        friend = self.api.create_friendship('twitter')
        self.assertEqual(friend.screen_name, 'twitter')

        self.api.update_friendship('twitter')

    def test_show_friendship(self):
        source, target = self.api.show_friendship(target_screen_name='twtiter')
        self.assertTrue(isinstance(source, Friendship))
        self.assertTrue(isinstance(target, Friendship))

    def test_get_settings(self):
        self.api.get_settings()

    def test_verify_credentials(self):
        self.assertNotEqual(self.api.verify_credentials(), False)

        # make sure that `me.status.entities` is not an empty dict
        me = self.api.verify_credentials(include_entities=True)
        self.assertTrue(me.status.entities)

        # `status` shouldn't be included
        me = self.api.verify_credentials(skip_status=True)
        self.assertFalse(hasattr(me, 'status'))

    def test_update_settings(self):
        self.api.update_settings(lang='en')

    def test_update_profile(self):
        original = self.api.me()
        profile = {
            'name': 'Tweepy test 123',
            'url': 'http://www.example.com',
            'location': 'pytopia',
            'description': 'just testing things out'
        }
        updated = self.api.update_profile(**profile)
        self.api.update_profile(
            name=original.name, url=original.url,
            location=original.location, description=original.description
        )

        for k, v in profile.items():
            if k == 'email':
                continue
            self.assertEqual(getattr(updated, k), v)

    def test_update_profile_bg(self):
        self.api.update_profile_background_image(user=1, tile=1)
        # TODO
        # self.api.update_profile_background_image(image='examples/bg.png')

    def test_update_profile_colors(self):
        original = self.api.me()
        updated = self.api.update_profile_colors(
            '000', '000', '000', '000', '000')

        # restore colors
        self.api.update_profile_colors(
            original.profile_background_color,
            original.profile_text_color,
            original.profile_link_color,
            original.profile_sidebar_fill_color,
            original.profile_sidebar_border_color
        )

        self.assertEqual(updated.profile_background_color, '000')
        self.assertEqual(updated.profile_text_color, '000')
        self.assertEqual(updated.profile_link_color, '000')
        self.assertEqual(updated.profile_sidebar_fill_color, '000')
        self.assertEqual(updated.profile_sidebar_border_color, '000')

    @unittest.skip('TODO')
    def test_upate_profile_image(self):
        self.api.update_profile_image('examples/profile.png')

    def test_list_blocks(self):
        self.api.list_blocks()

    def test_blocks_ids(self):
        self.api.blocks_ids()

    def test_create_destroy_block(self):
        self.api.create_block('twitter')
        self.api.destroy_block('twitter')
        self.api.create_friendship('twitter')  # restore

    def test_lookup_users(self):
        self.api.lookup_users(screen_names=['twitterapi', 'twitter'])

    def test_get_user(self):
        u = self.api.get_user('twitter')
        self.assertEqual(u.screen_name, 'twitter')

        u = self.api.get_user(783214)
        self.assertEqual(u.screen_name, 'twitter')

    def test_me(self):
        me = self.api.me()
        self.assertEqual(username, me.screen_name)

    def test_search_users(self):
        self.api.search_users('twitter')

    def test_contributees(self):
        self.api.contributees(screen_name='themattharris')

    def test_contributors(self):
        self.api.contributors(screen_name='twitterapi')

    def test_favorites(self):
        self.api.favorites()

    def test_create_destroy_favorite(self):
        self.api.create_favorite(4901062372)
        self.api.destroy_favorite(4901062372)

    @unittest.skip('FIXME lists test')
    def test_lists(self):
        self.api.lists()

    def test_list_timeline(self):
        self.api.list_timeline(slug='teams', owner_screen_name='MLS', count=1)

    def test_saved_searches(self):
        s = self.api.create_saved_search('test')
        self.api.saved_searches()
        self.assertEqual(self.api.get_saved_search(s.id).query, 'test')
        self.api.destroy_saved_search(s.id)

    def test_geo_apis(self):
        self.api.geo_id(place_id='c3f37afa9efcf94b')  # Austin, TX, USA
        self.api.similar_places(lat=37, long=-122, name='Twitter HQ')
        self.api.reverse_geocode(lat=30.267370168467806,
                                 long=-97.74261474609375)  # Austin, TX, USA

    def test_trends_apis(self):
        self.api.trends_place(id=1)
        self.api.trends_available()
        self.api.trends_closest(lat=37.781157, long=-122.400612831116)


if __name__ == '__main__':
    unittest.main()
