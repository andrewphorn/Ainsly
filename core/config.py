﻿import json, os

import __main__

from logger import LoggerClass

log = LoggerClass()

loc = os.path.dirname(__main__.__file__)

class conf(object):

    def __init__(self, defaults):
        self.data = {}
        self.default = defaults
        self.filename = 'config'

    def setConfig(self,f):
        self.filename = str(f)
        return self

    def loadConfig(self):
        log.debug("Loading Config")
        try:
            with open('%s/data/%s.json' % (loc, self.filename),'r') as f:
                self.data = json.loads(f.read())
            if self.data == {}:
                raise ValueError
        except Exception,e:
            log.warning("Error loading config: %s" % e)
            self.data = self.default
            self.saveConfig()
        finally:
            return self

    def saveConfig(self):
        log.debug("Saving Config")
        with open('%s/data/%s.json' % (loc, self.filename),'w') as f:
            f.write(json.dumps(self.data, indent=4))
            f.close()
        return self

    def set(self,key,value):
        self.data[key] = value
        return self

    def string(self,key):
        if key in self.data:
            return str(self.data[key])
        return ''

    def list(self,key):
        if key in self.data:
            return list(self.data[key])
        return []

    def dict(self,key):
        if key in self.data:
            return dict(self.data[key])
        return {}

    def int(self,key):
        if key in self.data:
            return int(self.data[key])
        return 0

    def float(self,key):
        if key in self.data:
            return float(self.data[key])
        return 0.0

    def bool(self,key):
        if key in self.data:
            return bool(self.data[key])
        return False

def confObject():
    default = {
        'admins': [],
        'server': 'irc.example.net',
        'port'  : '6667',
        'nickname': 'Harriot',
        'channels': [
            '#example',
            '#example2'
        ],
        'prefix': '!',
        'plugins': ['help'],
    }

    return conf(default).loadConfig()
