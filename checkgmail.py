#!/usr/bin/env python

import time
import urllib
from xml.dom import minidom

emails = []
while 1:
	feed = urllib.urlopen('https://mail.google.com/mail/feed/atom/')
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
	time.sleep(120)

