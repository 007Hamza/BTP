# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

import urllib
import urllib2
import time
import re

from tweepy2.error import TweepError
from tweepy2.utils import convert_to_utf8_str
from tweepy2.models import Model

re_path_template = re.compile(r':\w+')


def bind_api(**config):

    class APIMethod(object):

        path = '/%s.json' % config.get('path')
        payload_type = config.get('payload_type', None)
        payload_list = config.get('payload_list', False)
        allowed_param = config.get('allowed_param', [])
        method = config.get('method', 'GET')
        require_auth = config.get('require_auth', True)
        use_cache = config.get('use_cache', True)

        def __init__(self, api, args, kargs):
            # If authentication is required and no credentials
            # are provided, throw an error.
            if self.require_auth and not api.auth:
                raise TweepError('Authentication required!')

            self.api = api
            self.post_data = kargs.pop('post_data', None)
            self.retry_count = kargs.pop('retry_count', api.retry_count)
            self.retry_delay = kargs.pop('retry_delay', api.retry_delay)
            self.retry_errors = kargs.pop('retry_errors', api.retry_errors)
            self.headers = kargs.pop('headers', {})
            self.build_parameters(args, kargs)
            self.api_root = api.api_root
            self.get_header = api.get_header

            # Perform any path variable substitution
            self.build_path()

            self.scheme = 'https://'

            self.host = api.host

            # Manually set Host header to fix an issue in python 2.5
            # or older where Host is set including the 443 port.
            # This causes Twitter to issue 301 redirect.
            # See Issue https://github.com/tweepy/tweepy/issues/12
            self.headers['Host'] = self.host

        def build_parameters(self, args, kargs):
            self.parameters = {}
            for idx, arg in enumerate(args):
                if arg is None:
                    continue

                try:
                    self.parameters[self.allowed_param[idx]] = convert_to_utf8_str(arg)
                except IndexError:
                    raise TweepError('Too many parameters supplied!')

            for k, arg in kargs.items():
                if arg is None:
                    continue
                if k in self.parameters:
                    raise TweepError('Multiple values for parameter %s supplied!' % k)

                self.parameters[k] = convert_to_utf8_str(arg)

        def build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip(':')

                if name == 'user' and 'user' not in self.parameters and self.api.auth:
                    # No 'user' parameter provided, fetch it from Auth instead.
                    value = self.api.auth.get_username()
                elif name == 'id' and 'id' not in self.parameters and self.api.auth:
                    value = self.api.auth.get_user_id()
                else:
                    try:
                        value = urllib.quote(self.parameters[name])
                    except KeyError:
                        raise TweepError('No parameter value found for path variable: %s' % name)
                    del self.parameters[name]

                self.path = self.path.replace(variable, value)

        def execute(self):
            # Build the request URL
            url = self.api_root + self.path
            if len(self.parameters):
                url = '%s?%s' % (url, urllib.urlencode(self.parameters))

            if self.method == 'POST':
                if 'Content-Length' not in self.headers:
                    if self.post_data:
                        self.headers['Content-Length'] = len(self.post_data)
                    else:
                        self.headers['Content-Length'] = 0

            # Query the cache if one is available
            # and this request uses a GET method.
            if self.use_cache and self.api.cache and self.method == 'GET':
                cache_result = self.api.cache.get(url)
                # if cache result found and not expired, return it
                if cache_result:
                    # must restore api reference
                    if isinstance(cache_result, list):
                        for result in cache_result:
                            if isinstance(result, Model):
                                result._api = self.api
                    else:
                        if isinstance(cache_result, Model):
                            cache_result._api = self.api
                    return cache_result

            # Continue attempting request until successful
            # or maximum number of retries is reached.
            retries_performed = 0
            while True:
                # Apply authentication
                if self.api.auth:
                    self.api.auth.apply_auth(
                            self.scheme + self.host + url,
                            self.method, self.headers, self.parameters
                    )

                # Execute request
                # FIXME: add timeout
                try:
                    req = urllib2.Request(url=self.scheme + self.host + url, headers=self.headers, data=self.post_data)
                    req.get_method = lambda: self.method
                    if self.api.proxy_url:
                        proxy_url = 'http://%s' % self.api.proxy_url
                        proxy_handler = urllib2.ProxyHandler({'http': proxy_url, 'https': proxy_url})
                        opener = urllib2.build_opener(proxy_handler)
                        resp = opener.open(req)
                    else:
                        resp = urllib2.urlopen(req)
                    break
                except urllib2.HTTPError, e:
                    # continue request loop if retry error code
                    retry = retries_performed < self.retry_count
                    if self.retry_errors:
                        if e.code not in self.retry_errors:
                            retry = False
                    if retry:
                        retries_performed += 1
                        time.sleep(self.retry_delay)
                        continue

                    # Retry failed. throw an exception
                    try:
                        error_msg = self.api.parser.parse_error(e.read())
                    except Exception:
                        error_msg = "Twitter error response: status code = %s" % e.code
                    raise TweepError(error_msg)
                except Exception, e:
                    # any other exception is fatal
                    raise TweepError('Failed to send request: %s' % e)

            # Parse the response payload
            self.api.last_response = resp
            result = self.api.parser.parse(self, resp.read())

            if self.get_header:
                headers = dict(resp.info())
                if isinstance(result, dict):
                    result[u'_headers'] = headers
                elif isinstance(result, list):
                    tmp_result = {
                        u'_headers': headers,
                        u'ids': result,
                    }
                    result = tmp_result

            resp.close()

            # Store result into cache if one is available.
            if self.use_cache and self.api.cache and self.method == 'GET' and result:
                self.api.cache.store(url, result)

            return result

    def _call(api, *args, **kargs):

        method = APIMethod(api, args, kargs)
        return method.execute()

    # Set pagination mode
    if 'cursor' in APIMethod.allowed_param:
        _call.pagination_mode = 'cursor'
    elif 'since_id' in APIMethod.allowed_param:
        _call.pagination_mode = 'page'

    return _call
