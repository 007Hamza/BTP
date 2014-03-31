# -*- coding: utf-8 -*-
# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2012 sakito
# See LICENSE for details.
import subprocess


def get_version(version=None):
    """Returns PEP 386 version number"""
    if version is None:
        from tweepy2 import VERSION as version

    level_map = {
        'alpha': 'a',
        'beta': 'b',
        'rc': 'c',
        'final': None,
    }

    assert len(version) == 5
    assert version[3] in level_map.keys()

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    devn = ''
    if version[3] != 'final':
        devn += level_map.get(version[3]) + str(version[4])

    if version[3] == 'alpha' and version[4] == 0:
        hg_changeset = get_hg_changeset()
        if hg_changeset is not None:
            devn += '.dev%s' % hg_changeset

    return str(main + devn)


def get_hg_changeset():
    """Returs hg rev"""
    hg_tip = subprocess.Popen('hg tip --template "{rev}\n"',
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True,
                              universal_newlines=True)
    rev = hg_tip.communicate()[0].rstrip()
    return rev
