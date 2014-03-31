# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

import os
import mimetypes

from tweepy.binder import bind_api
from tweepy.error import TweepError
from tweepy.parsers import ModelParser
from tweepy.utils import list_to_csv


class API(object):
    """Twitter API"""

    def __init__(self, auth_handler=None,
            host='api.twitter.com', search_host='search.twitter.com',
            cache=None, api_root='/1', search_root='',
            retry_count=0, retry_delay=0, retry_errors=None, proxy_url=None,
            parser=None):
        self.auth = auth_handler
        if auth_handler:
            auth_handler.api = self
        self.host = host
        self.search_host = search_host
        self.api_root = api_root
        self.search_root = search_root
        self.cache = cache
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.proxy_url = proxy_url
        self.parser = parser or ModelParser()

    """ statuses/home_timeline """
    home_timeline = bind_api(
        path = 'statuses/home_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page', 'trim_user', 'include_entities'],
        require_auth = True
    )

    """ statuses/friends_timeline """
    friends_timeline = bind_api(
        path = 'statuses/friends_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page', 'trim_user', 'include_entities'],
        require_auth = True
    )

    """ statuses/user_timeline """
    user_timeline = bind_api(
        path = 'statuses/user_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['id', 'user_id', 'screen_name', 'since_id',
                          'max_id', 'count', 'page', 'include_rts',
                          'trim_user', 'include_entities']
    )

    """ statuses/mentions """
    mentions = bind_api(
        path = 'statuses/mentions',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page', 'trim_user', 'include_entities'],
        require_auth = True
    )

    """/statuses/retweeted_by_user.format"""
    retweeted_by_user = bind_api(
        path = 'statuses/retweeted_by_user',
        payload_type = 'status', payload_list = True,
        allowed_param = ['screen_name', 'id', 'count', 'since_id',
                            'max_id', 'page', 'include_entities']
    )

    """/statuses/:id/retweeted_by.format"""
    retweeted_by = bind_api(
        path = 'statuses/{id}/retweeted_by',
        payload_type = 'status', payload_list = True,
        allowed_param = ['id', 'count', 'page', 'include_entities'],
        require_auth = True
    )

    """/related_results/show/:id.format"""
    related_results = bind_api(
        path = 'related_results/show/{id}',
        payload_type = 'relation', payload_list = True,
        allowed_param = ['id'],
        require_auth = False
    )

    """/statuses/:id/retweeted_by/ids.format"""
    retweeted_by_ids = bind_api(
        path = 'statuses/{id}/retweeted_by/ids',
        payload_type = 'ids',
        allowed_param = ['id', 'count', 'page'],
        require_auth = True
    )

    """ statuses/retweeted_by_me """
    retweeted_by_me = bind_api(
        path = 'statuses/retweeted_by_me',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page', 'trim_user', 'include_entities'],
        require_auth = True
    )

    """ statuses/retweeted_to_me """
    retweeted_to_me = bind_api(
        path = 'statuses/retweeted_to_me',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page', 'trim_user', 'include_entities'],
        require_auth = True
    )

    """ statuses/retweets_of_me """
    retweets_of_me = bind_api(
        path = 'statuses/retweets_of_me',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page', 'trim_user', 'include_entities'],
        require_auth = True
    )

    """ statuses/show """
    get_status = bind_api(
        path = 'statuses/show',
        payload_type = 'status',
        allowed_param = ['id']
    )

    """ statuses/update """
    update_status = bind_api(
        path = 'statuses/update',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['status', 'in_reply_to_status_id', 'lat', 'long', 'source', 'place_id'],
        require_auth = True
    )

    """ statuses/destroy """
    destroy_status = bind_api(
        path = 'statuses/destroy',
        method = 'DELETE',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ statuses/retweet """
    retweet = bind_api(
        path = 'statuses/retweet/{id}',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ statuses/retweets """
    retweets = bind_api(
        path = 'statuses/retweets/{id}',
        payload_type = 'status', payload_list = True,
        allowed_param = ['id', 'count', 'trim_user', 'include_entities'],
        require_auth = True
    )

    """ users/show """
    get_user = bind_api(
        path = 'users/show',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name']
    )

    """ Perform bulk look up of users from user ID or screenname """
    def lookup_users(self, user_ids=None, screen_names=None):
        return self._lookup_users(list_to_csv(user_ids), list_to_csv(screen_names))

    _lookup_users = bind_api(
        path = 'users/lookup',
        payload_type = 'user', payload_list = True,
        allowed_param = ['user_id', 'screen_name'],
    )

    """ Get the authenticated user """
    def me(self):
        return self.get_user(screen_name=self.auth.get_username())

    """ users/search """
    search_users = bind_api(
        path = 'users/search',
        payload_type = 'user', payload_list = True,
        require_auth = True,
        allowed_param = ['q', 'per_page', 'page']
    )

    """ statuses/friends """
    friends = bind_api(
        path = 'statuses/friends',
        payload_type = 'user', payload_list = True,
        allowed_param = ['id', 'user_id', 'screen_name', 'page', 'cursor']
    )

    """ statuses/followers """
    followers = bind_api(
        path = 'statuses/followers',
        payload_type = 'user', payload_list = True,
        allowed_param = ['id', 'user_id', 'screen_name', 'page', 'cursor']
    )

    """ direct_messages """
    direct_messages = bind_api(
        path = 'direct_messages',
        payload_type = 'direct_message', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )

    """ direct_messages/show """
    get_direct_message = bind_api(
        path = 'direct_messages/show/{id}',
        payload_type = 'direct_message',
        allowed_param = ['id'],
        require_auth = True
    )

    """ direct_messages/sent """
    sent_direct_messages = bind_api(
        path = 'direct_messages/sent',
        payload_type = 'direct_message', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )

    """ direct_messages/new """
    send_direct_message = bind_api(
        path = 'direct_messages/new',
        method = 'POST',
        payload_type = 'direct_message',
        allowed_param = ['user', 'screen_name', 'user_id', 'text'],
        require_auth = True
    )

    """ direct_messages/destroy """
    destroy_direct_message = bind_api(
        path = 'direct_messages/destroy',
        method = 'DELETE',
        payload_type = 'direct_message',
        allowed_param = ['id'],
        require_auth = True
    )

    """ friendships/create """
    create_friendship = bind_api(
        path = 'friendships/create',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name', 'follow'],
        require_auth = True
    )

    """ friendships/destroy """
    destroy_friendship = bind_api(
        path = 'friendships/destroy',
        method = 'DELETE',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ friendships/exists """
    exists_friendship = bind_api(
        path = 'friendships/exists',
        payload_type = 'json',
        allowed_param = ['user_a', 'user_b']
    )

    """ friendships/show """
    show_friendship = bind_api(
        path = 'friendships/show',
        payload_type = 'friendship',
        allowed_param = ['source_id', 'source_screen_name',
                          'target_id', 'target_screen_name']
    )


    """ Perform bulk look up of friendships from user ID or screenname """
    def lookup_friendships(self, user_ids=None, screen_names=None):
	    return self._lookup_friendships(list_to_csv(user_ids), list_to_csv(screen_names))

    _lookup_friendships = bind_api(
        path = 'friendships/lookup',
        payload_type = 'relationship', payload_list = True,
        allowed_param = ['user_id', 'screen_name'],
        require_auth = True
    )


    """ friends/ids """
    friends_ids = bind_api(
        path = 'friends/ids',
        payload_type = 'ids',
        allowed_param = ['id', 'user_id', 'screen_name', 'cursor']
    )

    """ friendships/incoming """
    friendships_incoming = bind_api(
        path = 'friendships/incoming',
        payload_type = 'ids',
        allowed_param = ['cursor']
    )

    """ friendships/outgoing"""
    friendships_outgoing = bind_api(
        path = 'friendships/outgoing',
        payload_type = 'ids',
        allowed_param = ['cursor']
    )

    """ followers/ids """
    followers_ids = bind_api(
        path = 'followers/ids',
        payload_type = 'ids',
        allowed_param = ['id', 'user_id', 'screen_name', 'cursor']
    )

    """ account/verify_credentials """
    def verify_credentials(self, **kargs):
        try:
            return bind_api(
                path = 'account/verify_credentials',
                payload_type = 'user',
                require_auth = True,
                allowed_param = ['include_entities', 'skip_status'],
            )(self, **kargs)
        except TweepError, e:
            if e.response and e.response.status == 401:
                return False
            raise

    """ account/rate_limit_status """
    rate_limit_status = bind_api(
        path = 'account/rate_limit_status',
        payload_type = 'json',
        use_cache = False
    )

    """ account/update_delivery_device """
    set_delivery_device = bind_api(
        path = 'account/update_delivery_device',
        method = 'POST',
        allowed_param = ['device'],
        payload_type = 'user',
        require_auth = True
    )

    """ account/update_profile_colors """
    update_profile_colors = bind_api(
        path = 'account/update_profile_colors',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['profile_background_color', 'profile_text_color',
                          'profile_link_color', 'profile_sidebar_fill_color',
                          'profile_sidebar_border_color'],
        require_auth = True
    )

    """ account/update_profile_image """
    def update_profile_image(self, filename):
        headers, post_data = API._pack_image(filename, 700)
        return bind_api(
            path = 'account/update_profile_image',
            method = 'POST',
            payload_type = 'user',
            require_auth = True
        )(self, post_data=post_data, headers=headers)

    """ account/update_profile_background_image """
    def update_profile_background_image(self, filename, *args, **kargs):
        headers, post_data = API._pack_image(filename, 800)
        bind_api(
            path = 'account/update_profile_background_image',
            method = 'POST',
            payload_type = 'user',
            allowed_param = ['tile'],
            require_auth = True
        )(self, post_data=post_data, headers=headers)

    """ account/update_profile """
    update_profile = bind_api(
        path = 'account/update_profile',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['name', 'url', 'location', 'description'],
        require_auth = True
    )

    """ favorites """
    favorites = bind_api(
        path = 'favorites',
        payload_type = 'status', payload_list = True,
        allowed_param = ['id', 'max_id', 'page', 'include_entities']
    )

    """ favorites/create """
    create_favorite = bind_api(
        path = 'favorites/create/{id}',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ favorites/destroy """
    destroy_favorite = bind_api(
        path = 'favorites/destroy/{id}',
        method = 'DELETE',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ notifications/follow """
    enable_notifications = bind_api(
        path = 'notifications/follow',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ notifications/leave """
    disable_notifications = bind_api(
        path = 'notifications/leave',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ blocks/create """
    create_block = bind_api(
        path = 'blocks/create',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ blocks/destroy """
    destroy_block = bind_api(
        path = 'blocks/destroy',
        method = 'DELETE',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ blocks/exists """
    def exists_block(self, *args, **kargs):
        try:
            bind_api(
                path = 'blocks/exists',
                allowed_param = ['id', 'user_id', 'screen_name'],
                require_auth = True
            )(self, *args, **kargs)
        except TweepError:
            return False
        return True

    """ blocks/blocking """
    blocks = bind_api(
        path = 'blocks/blocking',
        payload_type = 'user', payload_list = True,
        allowed_param = ['page'],
        require_auth = True
    )

    """ blocks/blocking/ids """
    blocks_ids = bind_api(
        path = 'blocks/blocking/ids',
        payload_type = 'json',
        require_auth = True
    )

    """ report_spam """
    report_spam = bind_api(
        path = 'report_spam',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ saved_searches """
    saved_searches = bind_api(
        path = 'saved_searches',
        payload_type = 'saved_search', payload_list = True,
        require_auth = True
    )

    """ saved_searches/show """
    get_saved_search = bind_api(
        path = 'saved_searches/show/{id}',
        payload_type = 'saved_search',
        allowed_param = ['id'],
        require_auth = True
    )

    """ saved_searches/create """
    create_saved_search = bind_api(
        path = 'saved_searches/create',
        method = 'POST',
        payload_type = 'saved_search',
        allowed_param = ['query'],
        require_auth = True
    )

    """ saved_searches/destroy """
    destroy_saved_search = bind_api(
        path = 'saved_searches/destroy/{id}',
        method = 'DELETE',
        payload_type = 'saved_search',
        allowed_param = ['id'],
        require_auth = True
    )

    """ help/test """
    def test(self):
        try:
            bind_api(
                path = 'help/test',
            )(self)
        except TweepError:
            return False
        return True

    def create_list(self, *args, **kargs):
        return bind_api(
            path = '%s/lists' % self.auth.get_username(),
            method = 'POST',
            payload_type = 'list',
            allowed_param = ['name', 'mode', 'description'],
            require_auth = True
        )(self, *args, **kargs)

    def destroy_list(self, slug):
        return bind_api(
            path = '%s/lists/%s' % (self.auth.get_username(), slug),
            method = 'DELETE',
            payload_type = 'list',
            require_auth = True
        )(self)

    def update_list(self, slug, *args, **kargs):
        return bind_api(
            path = '%s/lists/%s' % (self.auth.get_username(), slug),
            method = 'POST',
            payload_type = 'list',
            allowed_param = ['name', 'mode', 'description'],
            require_auth = True
        )(self, *args, **kargs)

    lists = bind_api(
        path = '{user}/lists',
        payload_type = 'list', payload_list = True,
        allowed_param = ['user', 'cursor'],
        require_auth = True
    )

    lists_memberships = bind_api(
        path = '{user}/lists/memberships',
        payload_type = 'list', payload_list = True,
        allowed_param = ['user', 'cursor'],
        require_auth = True
    )

    lists_subscriptions = bind_api(
        path = '{user}/lists/subscriptions',
        payload_type = 'list', payload_list = True,
        allowed_param = ['user', 'cursor'],
        require_auth = True
    )

    list_timeline = bind_api(
        path = '{owner}/lists/{slug}/statuses',
        payload_type = 'status', payload_list = True,
        allowed_param = ['owner', 'slug', 'since_id', 'max_id', 'per_page', 'page', 'include_entities']
    )

    get_list = bind_api(
        path = '{owner}/lists/{slug}',
        payload_type = 'list',
        allowed_param = ['owner', 'slug']
    )

    list_members = bind_api(
        path = '{owner}/{slug}/members',
        payload_type = 'user', payload_list = True,
        allowed_param = ['owner', 'slug', 'cursor']
    )

    def is_list_member(self, owner, slug, user_id):
        try:
            return bind_api(
                path = '%s/%s/members/%s' % (owner, slug, user_id),
                payload_type = 'user'
            )(self)
        except TweepError:
            return False

    subscribe_list = bind_api(
        path = '{owner}/{slug}/subscribers',
        method = 'POST',
        payload_type = 'list',
        allowed_param = ['owner', 'slug'],
        require_auth = True
    )

    unsubscribe_list = bind_api(
        path = '{owner}/{slug}/subscribers',
        method = 'DELETE',
        payload_type = 'list',
        allowed_param = ['owner', 'slug'],
        require_auth = True
    )

    list_subscribers = bind_api(
        path = '{owner}/{slug}/subscribers',
        payload_type = 'user', payload_list = True,
        allowed_param = ['owner', 'slug', 'cursor']
    )

    def is_subscribed_list(self, owner, slug, user_id):
        try:
            return bind_api(
                path = '%s/%s/subscribers/%s' % (owner, slug, user_id),
                payload_type = 'user'
            )(self)
        except TweepError:
            return False

    """ trends/available """
    trends_available = bind_api(
        path = 'trends/available',
        payload_type = 'json',
        allowed_param = ['lat', 'long']
    )

    """ trends/location """
    trends_location = bind_api(
        path = 'trends/{woeid}',
        payload_type = 'json',
        allowed_param = ['woeid']
    )

    """ search """
    search = bind_api(
        search_api = True,
        path = 'search',
        payload_type = 'search_result', payload_list = True,
        allowed_param = ['q', 'lang', 'locale', 'rpp', 'page', 'since_id', 'geocode', 'show_user', 'max_id', 'since', 'until', 'result_type']
    )
    search.pagination_mode = 'page'

    """ trends/daily """
    trends_daily = bind_api(
        path = 'trends/daily',
        payload_type = 'json',
        allowed_param = ['date', 'exclude']
    )

    """ trends/weekly """
    trends_weekly = bind_api(
        path = 'trends/weekly',
        payload_type = 'json',
        allowed_param = ['date', 'exclude']
    )

    """ geo/reverse_geocode """
    reverse_geocode = bind_api(
        path = 'geo/reverse_geocode',
        payload_type = 'json',
        allowed_param = ['lat', 'long', 'accuracy', 'granularity', 'max_results']
    )

    """ geo/nearby_places """
    # listed as deprecated on twitter's API documents
    nearby_places = bind_api(
        path = 'geo/nearby_places',
        payload_type = 'json',
        allowed_param = ['lat', 'long', 'ip', 'accuracy', 'granularity', 'max_results']
    )

    """ geo/id """
    geo_id = bind_api(
        path = 'geo/id/{id}',
        payload_type = 'json',
        allowed_param = ['id']
    )

    """ geo/search """
    geo_search = bind_api(
        path = 'geo/search',
        payload_type = 'json',
        allowed_param = ['lat', 'long', 'query', 'ip', 'granularity', 'accuracy', 'max_results', 'contained_within']
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
