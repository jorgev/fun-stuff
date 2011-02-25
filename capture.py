#!/usr/bin/env python

import sys
import pycurl
import json

class Response:
	def __init__(self):
		self.contents = ''
	
	def body_callback(self, buf):
		self.contents = self.contents + buf

def main(argv=None):
	if argv is None:
		argv = sys.argv

	# we expect the file name to be passed in on the command line
	if len(argv) < 2:
		print 'No filename provided'
		return

	# arg should be filename
	filename = argv[1]

	# create the request object
	r = Response()
	c = pycurl.Curl()
	values = [('key', '45d2553f4d1cea074e85fc463fc1bc09'), ('image', (c.FORM_FILE, filename))]
	c.setopt(c.URL, "http://api.imgur.com/2/upload.json")
	c.setopt(c.HTTPPOST, values)
	c.setopt(c.WRITEFUNCTION, r.body_callback)
	c.perform()
	c.close()
	
	# print the response
	info = json.loads(r.contents)
	print info['upload']['links']['original']

if __name__ == '__main__':
	sys.exit(main())

