# -*- coding: utf-8 -*-
#
# Copyringt 2011 Kenichi Sato <ksato9700@gmail.com>
# 
import json

class TeamboxError(Exception):
    def __init__(self, errors):
        super(TeamboxError, self).__init__(
            "TeamboxError: %s: %s" % (errors['type'], errors['message']))
        
class TeamboxObject(object):
    sf = None

    @staticmethod
    def generate_obj(jsr):
        if 'errors' in jsr:
            raise TeamboxError(jsr['errors'])
        if TeamboxObject.sf:
            TeamboxObject.sf.write(json.dumps(jsr))
        try:
            return eval(jsr['type'])(jsr)
        except :
            print jsr
            raise

    def __str__(self):
        return str(map(lambda k: getattr(self, k),
                       filter(lambda n:n[0]!='_', dir(self))))


class List(TeamboxObject):
    def __init__(self, jsr): 
        self.objects = map(TeamboxObject.generate_obj, jsr['objects'])

class Project(TeamboxObject):
    def __init__(self, jsr): 
        map(lambda k: setattr(self,k,jsr[k]), jsr.keys())

