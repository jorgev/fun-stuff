#!/usr/bin/env python

import sys
import getpass
import base64
import time
import urllib2
from xml.dom import minidom

username = raw_input('Username: ')
password = getpass.getpass()
emails = []
req = urllib2.Request('https://mail.google.com/mail/feed/atom')
base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
auth_header = 'Basic %s' % base64string
req.add_header('Authorization', auth_header)
while 1:
	try:
		feed = urllib2.urlopen(req)
		doc = minidom.parse(feed)
		entries = doc.getElementsByTagName('entry')
		new_emails = []
		for entry in entries:
			id = entry.getElementsByTagName('id')[0].childNodes[0].data
			new_emails.append(id)
			if id in emails:
				continue
			title = entry.getElementsByTagName('title')[0].childNodes[0].data
			summary = entry.getElementsByTagName('summary')[0].childNodes[0].data
			name = entry.getElementsByTagName('author')[0].getElementsByTagName('name')[0].childNodes[0].data
			link = entry.getElementsByTagName('link')[0].getAttribute('href')
			print '%s - %s - %s - %s' % (name, title, summary, link)
		emails = new_emails
	except:
		print "Error while fetching feed: ", sys.exc_info()[0]
	time.sleep(120)

