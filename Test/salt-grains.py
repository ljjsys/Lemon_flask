#!/usr/bin/env python

import sys
import json
import urllib2
import re
import salt.log
import salt.utils
import salt.utils.network
import socket

def externalip ():
	grains = {}
	grains['external_ip4'] = urllib2.urlopen("http://api.ipify.org").read()

return grains





########################################################### 2

