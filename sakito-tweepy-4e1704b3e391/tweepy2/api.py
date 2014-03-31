# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

import os
import mimetypes

from tweepy2.binder import bind_api
from tweepy2.error import TweepError
from tweepy2.parsers import ModelParser
from tweepy2.utils import list_to_csv


class API(object):
    """Twitter API"""

    def __init__(self, auth_handler=None, cache=None,
                 retry_count=0, retry_delay=0, retry_errors=None,
                 proxy_url=None, parser=None, get_header=False):
        self.auth = auth_handler
        if auth_handler:
            auth_handler.api = self
        self.host = 'api.twitter.com'
        self.api_root = '/1.1'
        self.cache = cache
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.proxy_url = proxy_url
        self.parser = parser or ModelParser()
        self.get_header = get_header

    # statuses/mentions_timeline
    mentions_timeline = bind_api(
        path='statuses/mentions_timeline',
        payload_type='status',
        payload_list=True,
        allowed_param=['count', 'since_id', 'max_id', 'trim_user',
                       'contributor_details', 'include_entities'],
    )

    # statuses/user_timeline
    user_timeline = bind_api(
        path='statuses/user_timeline',
        payload_type='status',
        payload_list=True,
        allowed_param=['id', 'user_id', 'screen_name', 'since_id',
                       'count', 'max_id', 'trim_user', 'exclude_replies',
                       'contributor_details', 'include_rts'],
    )

    # statuses/home_timeline
    home_timeline = bind_api(
        path='statuses/home_timeline',
        payload_type='status',
        payload_list=True,
        allowed_param=['count', 'since_id', 'max_id', 'trim_user',
                       'exclude_replies', 'contributor_details',
                       'include_entities'],
    )

    # statuses/retweets_of_me
    retweets_of_me = bind_api(
        path='statuses/retweets_of_me',
        payload_type='status',
        payload_list=True,
        allowed_param=['count', 'since_id', 'max_id', 'trim_user',
                       'include_entities', 'include_user_entities'],
    )

    # tatuses/retweets
    retweets = bind_api(
        path='/statuses/retweets/:id',
        payload_type='status',
        payload_list=True,
        allowed_param=['id', 'count', 'trim_user'],
    )

    # statuses/show
    get_status = bind_api(
        path='statuses/show/:id',
        payload_type='status',
        allowed_param=['id', 'trim_user', 'include_my_retweet',
                       'include_entities'],
    )

    # statuses/destroy
    destroy_status = bind_api(
        path='statuses/destroy/:id',
        method='DELETE',
        payload_type='status',
        allowed_param=['id', 'trim_user'],
    )

    # statuses/update
    update_status = bind_api(
        path='statuses/update',
        method='POST',
        payload_type='status',
        allowed_param=['status', 'in_reply_to_status_id',
                       'lat', 'long', 'place_id', 'display_coordinates',
                       'trim_user'],
    )

    # statuses/retweet
    retweet = bind_api(
        path='statuses/retweet/:id',
        method='POST',
        payload_type='status',
        allowed_param=['id', 'trim_user'],
    )

    # statuses/update_with_media
    update_with_media = bind_api(
        path='statuses/update_with_media',
        method='POST',
        payload_type='json',
        allowed_param=['status', 'media[]', 'possibly_sensitive',
                       'in_reply_to_status_id', 'lat', 'long',
                       'place_id', 'display_coordinates'],
    )

    # statuses/oembed
    oembed = bind_api(
        path='statuses/oembed',
        payload_type='json',
        allowed_param=['id', 'url', 'maxwidth', 'hide_media', 'hide_thread',
                       'omit_script', 'align', 'related', 'lang'],
    )

    # search/tweets
    search_tweets = bind_api(
        path='search/tweets',
        payload_type='search_result',
        payload_list=True,
        allowed_param=['q', 'geocode', 'lang', 'locale', 'result_type',
                       'count', 'until', 'since_id', 'max_id',
                       'include_entities', 'callback'],
    )

    # direct_messages
    direct_messages = bind_api(
        path='direct_messages',
        payload_type='direct_message',
        payload_list=True,
        allowed_param=['since_id', 'max_id', 'count', 'page',
                       'include_entities', 'skip_status'],
    )

    # direct_messages/sent
    sent_direct_messages = bind_api(
        path='direct_messages/sent',
        payload_type='direct_message',
        payload_list=True,
        allowed_param=['since_id', 'max_id', 'count', 'page',
                       'include_entities'],
    )

    # direct_messages/show
    get_direct_message = bind_api(
        path='direct_messages/show',
        payload_type='direct_message',
        allowed_param=['id'],
    )

    # direct_messages/destroy
    destroy_direct_message = bind_api(
        path='direct_messages/destroy',
        method='DELETE',
        payload_type='direct_message',
        allowed_param=['id', 'include_entities'],
    )

    # direct_messages/new
    send_direct_message = bind_api(
        path='direct_messages/new',
        method='POST',
        payload_type='direct_message',
        allowed_param=['user', 'user_id', 'screen_name', 'text'],
    )

    # friends/ids
    friends_ids = bind_api(
        path='friends/ids',
        payload_type='ids',
        allowed_param=['id', 'user_id', 'screen_name',
                       'cursor', 'stringify_ids']
    )

    # followers/ids
    followers_ids = bind_api(
        path='followers/ids',
        payload_type='ids',
        allowed_param=['id', 'user_id', 'screen_name',
                       'cursor', 'stringify_ids']
    )

    # Perform bulk look up of friendships from user ID or screenname
    def lookup_friendships(self, user_ids=None, screen_names=None):
        return self._lookup_friendships(
            list_to_csv(user_ids), list_to_csv(screen_names))

    _lookup_friendships = bind_api(
        path='friendships/lookup',
        payload_type='relationship',
        payload_list=True,
        allowed_param=['user_id', 'screen_name'],
    )

    # friendships/incoming
    friendships_incoming = bind_api(
        path='friendships/incoming',
        payload_type='ids',
        allowed_param=['cursor', 'stringify_ids'],
    )

    # friendships/outgoing
    friendships_outgoing = bind_api(
        path='friendships/outgoing',
        payload_type='ids',
        allowed_param=['cursor', 'stringify_ids'],
    )

    # friendships/create
    create_friendship = bind_api(
        path='friendships/create',
        method='POST',
        payload_type='user',
        allowed_param=['id', 'user_id', 'screen_name', 'follow'],
    )

    # friendships/destroy
    destroy_friendship = bind_api(
        path='friendships/destroy',
        method='DELETE',
        payload_type='user',
        allowed_param=['id', 'user_id', 'screen_name'],
    )

    # friendships/update
    update_friendship = bind_api(
        path='friendships/update',
        method='POST',
        payload_type='user',
        allowed_param=['id', 'user_id', 'screen_name', 'device', 'retweets'],
    )

    # friendships/show
    show_friendship = bind_api(
        path='friendships/show',
        payload_type='friendship',
        allowed_param=['source_id', 'source_screen_name',
                       'target_id', 'target_screen_name']
    )

    # account/settings
    get_settings = bind_api(
        path='account/settings',
        payload_type='json',
    )

    # account/verify_credentials
    def verify_credentials(self, **kargs):
        try:
            return bind_api(
                path='account/verify_credentials',
                payload_type='user',
                require_auth=True,
                allowed_param=['include_entities', 'skip_status'],
            )(self, **kargs)
        except TweepError, e:
            if e.response and e.response.status == 401:
                return False
            raise

    # account/settings
    update_settings = bind_api(
        path='account/settings',
        method='POST',
        payload_type='json',
        allowed_param=['trend_location_woeid', 'sleep_time_enabled',
                       'start_sleep_time', 'end_sleep_time',
                       'time_zone', 'lang'],
    )

    # account/update_delivery_device
    set_delivery_device = bind_api(
        path='account/update_delivery_device',
        method='POST',
        payload_type='user',
        allowed_param=['device', 'include_entities'],
    )

    # account/update_profile
    update_profile = bind_api(
        path='account/update_profile',
        method='POST',
        payload_type='user',
        allowed_param=['name', 'url', 'location', 'description',
                       'include_entities', 'skip_status'],
    )

    # account/update_profile_background_image
    update_profile_background_image = bind_api(
        path='account/update_profile_background_image',
        method='POST',
        payload_type='user',
        allowed_param=['image', 'tile', 'include_entities',
                       'skip_status', 'use'],
    )

    # account/update_profile_colors
    update_profile_colors = bind_api(
        path='account/update_profile_colors',
        method='POST',
        payload_type='user',
        allowed_param=['profile_background_color',
                       'profile_link_color',
                       'profile_sidebar_border_color',
                       'profile_sidebar_fill_color',
                       'profile_text_color',
                       'include_entities', 'skip_status'],
    )

    # account/update_profile_image
    def update_profile_image(self, filename):
        headers, post_data = API._pack_image(filename, 700)
        return bind_api(
            path='account/update_profile_image',
            method='POST',
            payload_type='user',
            allowed_param=['image', 'include_entities', 'skip_status'],
        )(self, post_data=post_data, headers=headers)

    # blocks/list
    list_blocks = bind_api(
        path='blocks/list',
        payload_type='json',
        allowed_param=['include_entities', 'skip_status', 'cursor'],
    )

    # blocks/ids
    blocks_ids = bind_api(
        path='blocks/ids',
        payload_type='json',
        allowed_param=['stringify_ids', 'cursor'],
    )

    # blocks/create
    create_block = bind_api(
        path='blocks/create',
        method='POST',
        payload_type='user',
        allowed_param=['id', 'user_id', 'screen_name',
                       'include_entities', 'skip_status'],
    )

    # blocks/destroy
    destroy_block = bind_api(
        path='blocks/destroy',
        method='DELETE',
        payload_type='user',
        allowed_param=['id', 'user_id', 'screen_name',
                       'include_entities', 'skip_status'],
    )

    # Perform bulk look up of users from user ID or screenname
    def lookup_users(self, user_ids=None, screen_names=None):
        return self._lookup_users(list_to_csv(user_ids), list_to_csv(screen_names))

    _lookup_users = bind_api(
        path='users/lookup',
        payload_type='user',
        payload_list=True,
        allowed_param=['user_id', 'screen_name', 'include_entities'],
    )

    # users/show
    get_user = bind_api(
        path='users/show',
        payload_type='user',
        allowed_param=['id', 'user_id', 'screen_name', 'include_entities']
    )

    # Get the authenticated user
    def me(self):
        return self.get_user(screen_name=self.auth.get_username())

    # users/search
    search_users = bind_api(
        path='users/search',
        payload_type='user',
        payload_list=True,
        allowed_param=['q', 'page', 'count', 'include_entities'],
    )

    # users/contributees
    contributees = bind_api(
        path='users/contributees',
        payload_type='user',
        payload_list=True,
        allowed_param=['user_id', 'screen_name',
                       'include_entities', 'skip_status'],
    )

    # users/contributors
    contributors = bind_api(
        path='users/contributors',
        payload_type='user',
        payload_list=True,
        allowed_param=['user_id', 'screen_name',
                       'include_entities', 'skip_status'],
    )

    # TODO
    # users/suggestions/:slug
    # users/suggestions
    # users/suggestions/:slug/members

    # favorites/list
    favorites = bind_api(
        path='favorites/list',
        payload_type='status',
        payload_list=True,
        allowed_param=['id', 'user_id', 'screen_name', 'count',
                       'since_id', 'max_id', 'include_entities'],
    )

    # favorites/destroy
    destroy_favorite = bind_api(
        path='favorites/destroy',
        method='DELETE',
        payload_type='status',
        allowed_param=['id', 'include_entities'],
    )

    # favorites/create
    create_favorite = bind_api(
        path='favorites/create',
        method='POST',
        payload_type='status',
        allowed_param=['id', 'include_entities'],
    )

    # lists/list
    lists = bind_api(
        path='lists/list',
        payload_type='list',
        payload_list=True,
        allowed_param=['user', 'user_id', 'screen_name'],
    )

    # lists/statuses
    list_timeline = bind_api(
        path='lists/statuses',
        payload_type='status',
        payload_list=True,
        allowed_param=['list_id', 'slug', 'owner_screen_name', 'owner_id',
                       'since_id', 'max_id', 'count',
                       'include_entities', 'include_rts'],
    )

    # lists/members/destroy
    remove_list_member = bind_api(
        path='lists/members/destroy',
        method='DELETE',
        payload_type='list',
        allowed_param=['list_id', 'slug', 'user_id', 'screen_name'],
    )

    # lists/memberships
    lists_memberships = bind_api(
        path='lists/memberships',
        payload_type='list',
        payload_list=True,
        allowed_param=['user', 'user_id', 'screen_name',
                       'cursor', 'filter_to_owned_lists'],
    )

    # lists/subscribers
    list_subscribers = bind_api(
        path='lists/subscribers',
        payload_type='list',
        allowed_param=['list_id', 'slug', 'owner',
                       'owner_screen_name', 'owner_id', 'cursor',
                       'include_entities', 'skip_status'],
    )

    # lists/subscribers/create
    create_list_subscribers = bind_api(
        path='lists/subscribers/create',
        method='POST',
        payload_type='list',
        allowed_param=['owner_screen_name', 'owner_id', 'list_id', 'slug'],
    )

    # lists/subscribers/show
    get_lists_subscribers = bind_api(
        path='lists/subscribers/show',
        payload_type='list',
        allowed_param=['owner_screen_name', 'owner_id', 'list_id', 'slug',
                       'user_id', 'screen_name',
                       'include_entities', 'skip_status'],
    )

    def is_subscribed_list(self, owner, slug, user_id):
        try:
            return self.get_lists_subscribers(
                owner=owner, slug=slug, user_id=user_id)
        except TweepError:
            return False

    # lists/subscribers/destroy
    remove_lists_subscribers = bind_api(
        path='lists/subscribers/destroy',
        method='DELETE',
        payload_type='list',
        allowed_param=['list_id', 'slug', 'owner_screen_name', 'owner_id'],
    )

    # lists/members/create_all
    add_lists_members = bind_api(
        path='lists/members/create_all',
        method='POST',
        payload_type='list',
        allowed_param=['list_id', 'slug', 'user_id', 'screen_name',
                       'owner_screen_name', 'owner_id '],
    )

    # lists/members/show
    list_members = bind_api(
        path='lists/members/show',
        payload_type='user',
        payload_list=True,
        allowed_param=['list_id', 'slug', 'user_id', 'screen_name',
                       'owner_screen_name', 'owner_id',
                       'include_entities', 'skip_status'],
    )

    def is_list_member(self, owner, slug, user_id):
        try:
            return self.list_members(owner=owner, slug=slug, user_id=user_id)
        except TweepError:
            return False

    # lists/destroy
    destroy_list = bind_api(
        path='lists/destroy',
        method='DELETE',
        ayload_type='list',
        allowed_param=['owner_screen_name', 'owner_id', 'list_id', 'slug'],
    )

    # lists/update
    update_list = bind_api(
        path='lists/update',
        method='POST',
        payload_type='list',
        allowed_param=['list_id', 'slug', 'name', 'mode', 'description',
                       'owner_screen_name', 'owner_id'],
    )

    # lists/create
    create_list = bind_api(
        path='lists/create',
        method='POST',
        payload_type='list',
        allowed_param=['name', 'mode', 'description'],
    )

    # lists/show
    get_list = bind_api(
        path='lists/show',
        payload_type='list',
        allowed_param=['list_id', 'slug', 'owner_screen_name', 'owner_id'],
    )

    # lists/subscriptions
    lists_subscriptions = bind_api(
        path='lists/subscriptions',
        payload_type='list',
        payload_list=True,
        allowed_param=['user', 'user_id', 'screen_name', 'count', 'cursor'],
    )

    # lists/members/destroy_all
    remove_list_members = bind_api(
        path='lists/members/destroy_all',
        payload_type='list',
        payload_list=True,
        allowed_param=['list_id', 'slug', 'user_id', 'screen_name',
                       'owner_screen_name', 'owner_id'],
    )

    # saved_searches/list
    saved_searches = bind_api(
        path='saved_searches/list',
        payload_type='saved_search',
        payload_list=True,
    )

    # saved_searches/show/:id
    get_saved_search = bind_api(
        path='saved_searches/show/:id',
        payload_type='saved_search',
        allowed_param=['id'],
    )

    # saved_searches/create
    create_saved_search = bind_api(
        path='saved_searches/create',
        method='POST',
        payload_type='saved_search',
        allowed_param=['query'],
    )

    # saved_searches/destroy/:id
    destroy_saved_search = bind_api(
        path='saved_searches/destroy/:id',
        method='DELETE',
        payload_type='saved_search',
        allowed_param=['id'],
    )

    # geo/id/:place_id
    geo_id = bind_api(
        path='geo/id/:place_id',
        payload_type='json',
        allowed_param=['place_id'],
    )

    # geo/reverse_geocode
    reverse_geocode = bind_api(
        path='geo/reverse_geocode',
        payload_type='json',
        allowed_param=['lat', 'long', 'accuracy', 'granularity',
                       'max_results', 'callback'],
    )

    # geo/search
    geo_search = bind_api(
        path='geo/search',
        payload_type='json',
        allowed_param=['lat', 'long', 'query', 'ip', 'granularity',
                       'accuracy', 'max_results', 'contained_within',
                       'attribute:street_address', 'callback'],
    )

    # geo/similar_places
    similar_places = bind_api(
        path='geo/similar_places',
        payload_type='json',
        allowed_param=['lat', 'long', 'ip', 'name', 'contained_within',
                       'attribute:street_address', 'callback'],
    )

    # geo/place
    create_geo_place = bind_api(
        path='geo/place',
        method='POST',
        payload_type='json',
        allowed_param=['name', 'contained_within', 'token', 'lat', 'long',
                       'attribute:street_address', 'callback'],
    )

    # trends/place
    trends_place = bind_api(
        path='trends/place',
        payload_type='json',
        allowed_param=['id', 'exclude'],
    )

    # trends/available
    trends_available = bind_api(
        path='trends/available',
        payload_type='json',
    )

    # trends/closest
    trends_closest = bind_api(
        path='trends/closest',
        payload_type='json',
        allowed_param=['lat', 'long'],
    )

    # report_spam
    report_spam = bind_api(
        path='report_spam',
        method='POST',
        payload_type='user',
        allowed_param=['id', 'user_id', 'screen_name'],
    )

    # application/rate_limit_status
    rate_limit_status = bind_api(
        path='application/rate_limit_status',
        payload_type='json',
        use_cache=False,
        allowed_param=['resources'],
    )

    """ Internal use only """
    @staticmethod
    def _pack_image(filename, max_size):
        """Pack image from file into multipart-formdata post body"""
        # image must be less than 700kb in size
        try:
            if os.path.getsize(filename) > (max_size * 1024):
                raise TweepError('File is too big, must be less than 700kb.')
        except os.error:
            raise TweepError('Unable to access file')

        # image must be gif, jpeg, or png
        file_type = mimetypes.guess_type(filename)
        if file_type is None:
            raise TweepError('Could not determine file type')
        file_type = file_type[0]
        if file_type not in ['image/gif', 'image/jpeg', 'image/png']:
            raise TweepError('Invalid file type for image: %s' % file_type)

        # build the mulitpart-formdata body
        fp = open(filename, 'rb')
        BOUNDARY = 'Tw3ePy'
        body = []
        body.append('--' + BOUNDARY)
        body.append('Content-Disposition: form-data; name="image"; filename="%s"' % filename)
        body.append('Content-Type: %s' % file_type)
        body.append('')
        body.append(fp.read())
        body.append('--' + BOUNDARY + '--')
        body.append('')
        fp.close()
        body = '\r\n'.join(body)

        # build headers
        headers = {
            'Content-Type': 'multipart/form-data; boundary=Tw3ePy',
            'Content-Length': str(len(body))
        }

        return headers, body
