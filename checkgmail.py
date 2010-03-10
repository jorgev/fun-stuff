#!/usr/bin/env python

import sys
import getpass
import base64
import time
import urllib2
from xml.dom import minidom

# accept the user name and password
username = raw_input('Username: ')
password = getpass.getpass()

# set up the request info
req = urllib2.Request('https://mail.google.com/mail/feed/atom')
base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
auth_header = 'Basic %s' % base64string
req.add_header('Authorization', auth_header)

# this will hold the current list of email ids
emails = []
while 1:
	try:
		# connect to the gmail atom feed
		feed = urllib2.urlopen(req)

		# load the feed into our parser
		doc = minidom.parse(feed)

		# get the entry elements
		entries = doc.getElementsByTagName('entry')

		# this will be used to update the global current list
		new_emails = []

		# now iterate through the entries
		entries.reverse()
		for entry in entries:
			# get the message id
			id = entry.getElementsByTagName('id')[0].childNodes[0].data
			new_emails.append(id)

			# if we already dumped this email to the console, move on to the next one
			if id in emails:
				continue

			# get the other values of interest to us
			title = '(no subject)'
			if len(entry.getElementsByTagName('title')[0].childNodes) > 0:
				title = entry.getElementsByTagName('title')[0].childNodes[0].data
			summary = '(empty)'
			if len(entry.getElementsByTagName('summary')[0].childNodes) > 0:
				summary = entry.getElementsByTagName('summary')[0].childNodes[0].data
			name = entry.getElementsByTagName('author')[0].getElementsByTagName('name')[0].childNodes[0].data
			link = entry.getElementsByTagName('link')[0].getAttribute('href')

			# dump the message info out to the console
			print '%s - %s - %s - %s' % (name, title, summary, link)
		emails = new_emails
	except Exception, reason:
		# we just swallow errors, typically they are random connection failures
		print reason
	time.sleep(120)

