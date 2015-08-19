#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
Connection to the Testrail server.

Manages Url, Credentials. Handles HTTP Error codes.
"""

from __future__ import absolute_import
from __future__ import print_function

import json
from collections import defaultdict

try:
    import requests
    import requests.auth as auth
except ImportError:
    raise RuntimeError('Module "requests" is required. Maybe "pip install requests"?')


import testrail.core.errors as errors


class TestrailConnection(object):

    def __init__(self, server_address, user, password):
        if not server_address.startswith('http'):
            server_address = 'http://' + server_address

        self.base_url = server_address + '/testrail/index.php?/api/v2/'

        self.session = requests.Session()

        self.session.headers.update({
            'Content-Type': 'application/json'
        })

        self.session.auth = auth.HTTPBasicAuth(user, password)

    ############################################################################
    # Shortcuts to access API by relative path and do common error processing

    def get(self, url, **kwargs):
        print('GET ', url, kwargs)  # debug

        result = self.session.get(self.base_url + url, **kwargs)

        return self.process_result(result)

    def post(self, url, data=None, **kwargs):
        print('POST', url, data, kwargs)  # debug

        if data is not None:
            result = self.session.post(self.base_url + url,
                                       data=json.dumps(data),
                                       **kwargs)
        else:
            result = self.session.post(self.base_url + url,
                                       **kwargs)

        return self.process_result(result)

    @staticmethod
    def process_result(result):
        if result.status_code == 200:
            print(result.text[:2048])  # debug
            try:
                return json.loads(result.text)
            except ValueError:
                # empty response
                return None

        elif result.status_code in [400, 404]:
            raise errors.NotFoundError(result.json()['error'])
        elif result.status_code == 401:
            raise errors.AuthenticationError(result.json()['error'])
        elif result.status_code == 403:
            raise errors.AccessError(result.json()['error'])
        else:
            raise errors.TestrailError('HTTP Error! %s: %s' % (result.status_code, result.reason))
