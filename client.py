# -*- coding: utf-8 -*-
#
# Copyringt 2011 Kenichi Sato <ksato9700@gmail.com>
# 
import urllib2
import json
import base64

from model import TeamboxObject

URL_PREFIX = "https://teambox.com/api/1/"
debug = 100

class TeamboxClient(object):
    def __init__(self, credential=None):
        self.headers = {
            'Accept': 'application/json',
            }
        if credential:
            self.headers['Authorization'] = "Basic %s" % base64.b64encode(credential).strip()

        self.openr = urllib2.build_opener(urllib2.HTTPCookieProcessor(),
                                          urllib2.HTTPSHandler(debug),
                                          )

    def _make_request(self, command, params=None, headers={}):
        if params:
            data = urllib.urlencode(params)
        else:
            data = None

        headers.update(self.headers)
        try:
            url = URL_PREFIX + command
            #print url
            f = self.openr.open(urllib2.Request(url=url,
                                                data=data,
                                                headers=headers))

            response = TeamboxObject.generate_obj(json.load(f))
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

    #TeamboxObject.sf = open("jsr.json", "w")
    response = client.projects()
    print response
    #TeamboxObject.sf.close()

if __name__ == "__main__":
    main()
