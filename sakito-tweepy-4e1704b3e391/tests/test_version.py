# -*- coding: utf-8 -*-
# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2012 sakito
# See LICENSE for details.
from __future__ import with_statement

import unittest

import tweepy
import tweepy2
from tweepy2 import version


class VersionTest(unittest.TestCase):

    def test_get_version(self):
        self.assertEquals(version.get_version(tweepy2.VERSION),
                          version.get_version())

        VERSION = (2, 0, 5, 'alpha', 1)
        self.assertEquals('2.0.5a1', version.get_version(VERSION))

        VERSION = (2, 0, 5, 'alpha', 0)
        self.assertEquals('2.0.5a0.dev571',
                          version.get_version(VERSION))

        VERSION = (2, 0, 5, 'foo', 1)
        self.assertRaises(AssertionError, version.get_version, VERSION)

    def test_get_hg_changeset(self):
        self.assertEqual('571', version.get_hg_changeset())

    def test_api_version(self):
        api = tweepy.API()
        self.assertEqual('/1', api.api_root)
        self.assertEqual('1', tweepy.API_VERSION)

        api = tweepy2.API()
        self.assertEqual('/1.1', api.api_root)
        self.assertEqual('1.1', tweepy2.API_VERSION)

if __name__ == '__main__':
    unittest.main()
