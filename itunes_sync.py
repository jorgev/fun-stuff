#!/usr/bin/env python
# encoding: utf-8
"""
itunes_sync.py

Created by Jorge Velázquez on 2010-09-18.
Copyright (c) 2010. All rights reserved.
"""

import sys
import getopt
from xml.dom import minidom

help_message = '''
-i <path to iTunes library xml file> (e.g., /Users/jorge/Music/iTunes/iTunes Music Library.xml)
-p <name of playlist to copy>
-o <path to music folder on android device> (e.g., /Volumes/)
'''

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hi:p:o:v", ["help", "input=", "playlist=", "output="])
		except getopt.error, msg:
			raise Usage(msg)
	
		# option processing
		input = None
		playlist = None
		output = None
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-i", "--input"):
				input = value
			if option in ("-p", "--playlist"):
				playlist = value
			if option in ("-o", "--output"):
				output = value
		
		# all options are required
		if not input or not playlist or not output:
			raise Usage('input, playlist, and output options are all required')
			return 3
		
		doc = minidom.parse(input)
		plist = doc.firstChild
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2
	except Exception, err:
		print >> sys.stderr, err
		return 3
	
	doc = minidom.parse(input)

if __name__ == "__main__":
	sys.exit(main())
