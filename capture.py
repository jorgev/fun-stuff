#!/usr/bin/env python

import sys
import base64
import getpass
import httplib

def main(argv=None):
	if argv is None:
		argv = sys.argv

	# we expect the file name to be passed in on the command line
	if len(argv) < 2:
		print 'No filename provided'
		return

	# prompt user for credentials
	username = raw_input('Username: ')
	password = getpass.getpass()

	# first, make sure we can read the file
	filename = argv[1]
	print 'Reading %s...' % filename
	file = open(filename, 'r')
	image_bytes = file.read()
	file.close()
	print '%d bytes read' % len(image_bytes)

	# don't allow an upload > 1MB
	if len(image_bytes) > (1024 * 1024):
		print 'Cannot upload files larger than 1MB'
		return

	# set up our connection
	conn = httplib.HTTPSConnection('jorge-v.appspot.com')
	auth = base64.b64encode('%s:%s' % (username, password))
	auth_header = 'Basic %s' % auth
	headers = { 'Content-Type': 'image/png', 'Authorization': auth_header }
	conn.request('PUT', '/capture/', image_bytes, headers)

	# get the response and dump the body
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	print data # entity should contain the URI for the new resource
	conn.close()

if __name__ == '__main__':
	sys.exit(main())

