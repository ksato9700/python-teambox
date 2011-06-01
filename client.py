# -*- coding: utf-8 -*-
#
# Copyringt 2011 Kenichi Sato <ksato9700@gmail.com>
# 
import urllib2
import json
import base64

URL_PREFIX = "https://teambox.com/api/1/"
debug = 100

class TeamboxError(Exception):
    def __init__(self, errors):
        super(TeamboxError, self).__init__(
            "TeamboxError: %s: %s" % (errors['type'], errors['message']))
        

class TeamboxClient(object):
    def __init__(self, credential=None):
        self.headers = {}
        if credential:
            self.headers['Authorization'] = "Basic %s" % base64.b64encode(credential).strip()

        self.openr = urllib2.build_opener(urllib2.HTTPCookieProcessor(),
                                          urllib2.HTTPSHandler(debug),
                                          )
        self.sf = None

    def _make_request(self, command, params=None):
        if params:
            data = urllib.urlencode(params)
        else:
            data = None

        headers = {}
        headers.update(self.headers)
        try:
            url = URL_PREFIX + command
            print url
            f = self.openr.open(urllib2.Request(url=url,
                                                data=data,
                                                headers=headers))
            response = json.load(f)
            if 'errors' in response:
                raise TeamboxError(response['errors'])
            if self.sf:
                self.sf.write(json.dumps(response))
            return response
            
        except urllib2.HTTPError as e:
            if e.code == 401:
                raise
            else:
                raise

    def projects(self):
        return self._make_request('projects')

def main():
    import sys

    client = TeamboxClient(sys.argv[1])
    response = client.projects()
    print json.dumps(response, indent=4)

if __name__ == "__main__":
    main()
