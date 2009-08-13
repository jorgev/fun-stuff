#!/usr/bin/env python
# encoding: utf-8
"""
twitter.py

Created by Jorge Velázquez on 2009-08-13.
"""

import sys
import getopt
import json
import urllib2

help_message = '''
Must provide a twitter username using -u or --user
'''

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hu:v", ["help", "user="])
		except getopt.error, msg:
			raise Usage(msg)
	
		# option processing
		user = None
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-u", "--user"):
				user = value
				
		if user is None:
			raise Usage(help_message)
	
		# here's the cool stuff, all in one line of code - get a json response with the statuses
		statuses = json.load(urllib2.urlopen('http://twitter.com/statuses/user_timeline/' + user + '.json'))
		print "%s statuses fetched, dumping..." % len(statuses)
		
		for status in statuses:
			print status['text'] + ' - ' + status['created_at']
		
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2

if __name__ == "__main__":
	sys.exit(main())
