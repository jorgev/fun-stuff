#!/usr/bin/env python

import sys
import base64
import getpass
import urllib
import urllib2
import cookielib

def main(argv=None):
	if argv is None:
		argv = sys.argv

	# we expect the file name to be passed in on the command line
	if len(argv) < 2:
		print 'No filename provided'
		return

	# first, make sure we can read the file
	filename = argv[1]
	print 'Reading %s...' % filename
	try:
		file = open(filename, 'r')
		image_bytes = file.read()
		file.close()
	except Exception, reason:
		print reason
		return
	print '%d bytes read' % len(image_bytes)

	# don't allow an upload > 1MB
	if len(image_bytes) > (1024 * 1024):
		print 'Cannot upload files larger than 1MB'
		return

	# prompt user for credentials
	username = raw_input('Email: ')
	password = getpass.getpass('Password for %s:' % username)

	# build up a url opener that supports cookies
	opener = urllib2.OpenerDirector()
	opener.add_handler(urllib2.ProxyHandler())
	opener.add_handler(urllib2.UnknownHandler())
	opener.add_handler(urllib2.HTTPHandler())
	opener.add_handler(urllib2.HTTPDefaultErrorHandler())
	opener.add_handler(urllib2.HTTPSHandler())
	opener.add_handler(urllib2.HTTPErrorProcessor())
	cookies = cookielib.MozillaCookieJar()
	opener.add_handler(urllib2.HTTPCookieProcessor(cookies))

	# get an auth ticket from google
	params = urllib.urlencode({ 'Email': username, 'Passwd': password, 'service': 'ah', 'source': 'jorge-v', 'accountType': 'HOSTED_OR_GOOGLE' })
	request = urllib2.Request('https://www.google.com/accounts/ClientLogin', params);
	try:
		response = opener.open(request)
	except urllib2.HTTPError, e:
		print e
		return
	data = response.read()
	auth = data.split('\n')[2].split('=')[1]

	# set up our image upload
	continue_url = 'https://jorge-v.appspot.com/capture'
	args = { 'continue': continue_url, 'auth': auth }
	cookie_url = 'https://jorge-v.appspot.com/_ah/login?%s' % urllib.urlencode(args)
	request = urllib2.Request(cookie_url)
	try:
		response = opener.open(request)
	except urllib2.HTTPError, e:
		if e.code != 302 or e.info()['location'] != continue_url:
			print e
			return
	headers = { 'Content-Type': 'image/png' }
	request = urllib2.Request(continue_url, image_bytes, headers)
	try:
		response = opener.open(request)
	except urllib2.HTTPError, e:
		print e
		return
	data = response.read()
	print data # entity should contain the URI for the new resource

if __name__ == '__main__':
	sys.exit(main())

