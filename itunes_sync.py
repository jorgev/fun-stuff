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
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2
	
	doc = minidom.parse(input)

if __name__ == "__main__":
	sys.exit(main())
