#!/usr/bin/env python

import sys
import getpass
import time
import urllib
import urllib2
import cookielib
import htmllib
import formatter
from xml.dom import minidom

entries = []
pages = []
current_page_index = 0

# this is our class to handle redirects
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):     
	def http_error_301(self, req, fp, code, msg, headers):  
		result = urllib2.HTTPRedirectHandler.http_error_301( 
			self, req, fp, code, msg, headers)              
		result.status = code                                 
		return result                                       

	def http_error_302(self, req, fp, code, msg, headers):   
		result = urllib2.HTTPRedirectHandler.http_error_302(
			self, req, fp, code, msg, headers)              
		result.status = code                                
		return result

# this class holds our row data
class Entry():
	def __init__(self):
		self.date = None
		self.time = None
		self.timestamp = None
		self.toFrom = None
		self.type = None
		self.direction = None

# this is our class to parse the HTML
class ATTParser(htmllib.HTMLParser):
	def __init__(self, formatter):
		self.in_table = False
		self.in_body = False
		self.in_ul = False
		self.current_row = None
		self.column_index = 0
		self.result = ''
		htmllib.HTMLParser.__init__(self, formatter)

	def start_table(self, attributes):
		for attribute in attributes:
			if attribute[0] == 'id' and attribute[1] == 'curRow': # this is the id for the table with the data usage
				self.in_table = True

	def end_table(self):
		self.in_table = False

	def start_tbody(self, attributes):
		if self.in_table:
			self.in_body = True

	def end_tbody(self):
		if self.in_table:
			self.in_body = False

	def start_tr(self, attributes):
		if self.in_body:
			self.current_row = Entry() # start a new row entry
			self.column_index = 0 # reset the column index

	def end_tr(self):
		if self.in_body and self.current_row:
			entries.append(self.current_row) # we're at the end of the row, append the current row to our list of entries
			self.current_row = None # and set the current row to nothing

	def start_td(self, attributes):
		self.result = '' # new table data, reset the variable we use to hold the data

	def end_td(self):
		if self.in_body and self.current_row:
			self.result = self.result.strip() # remove leading and trailing whitespace
			if self.column_index == 0:
				self.current_row.date = self.result
			elif self.column_index == 1:
				self.current_row.time = self.result
			elif self.column_index == 2:
				self.current_row.toFrom = self.result
			elif self.column_index == 3:
				self.current_row.type = self.result
			elif self.column_index == 4:
				self.current_row.direction = self.result
			self.column_index += 1

	def start_a(self, attributes):
		if self.in_ul:
			for attribute in attributes:
				if attribute[0] == 'href':
					page = attribute[1]
					if not page in pages: # make sure pages get added just once
						pages.append(page)

	def end_a(self):
		return

	def start_ul(self, attributes):
		for attribute in attributes:
			if attribute[0] == 'class' and attribute[1] == 'pagination':
				self.in_ul = True # we're in the list that has the page links

	def end_ul(self):
		self.in_ul = False

	def handle_data(self, data):
		if data:
			self.result += data # just keep appending

# accept the phone number and password
phone = raw_input('AT&T Phone # (numbers only, no dashes or spaces): ')
password = getpass.getpass()

# build up a url opener that supports cookies
opener = urllib2.OpenerDirector()
opener.add_handler(SmartRedirectHandler())
opener.add_handler(urllib2.ProxyHandler())
opener.add_handler(urllib2.UnknownHandler())
opener.add_handler(urllib2.HTTPHandler())
opener.add_handler(urllib2.HTTPDefaultErrorHandler())
opener.add_handler(urllib2.HTTPSHandler())
opener.add_handler(urllib2.HTTPErrorProcessor())
cookies = cookielib.MozillaCookieJar()
opener.add_handler(urllib2.HTTPCookieProcessor(cookies))

# here we make a POST to the login page, which will return 302 and we redirect to that page
params = urllib.urlencode({ 'reportActionEvent': 'A_LGN_LOGIN_SUB', 'loginType': 'WIRELESS', 'actionEvent': 'preAuthenticate', 'ajaxSupported': '', 'domain': '.att.com', 'wireless_num': phone, 'pass': password })
req = urllib2.Request('https://www.wireless.att.com//olam/loginAction.doview', params)

# connect to att login page
response = opener.open(req)

# push the first page on to the array, others will be added from links
pages.append('/olam/gotoDataDetailsAction.olamexecute?reportActionEvent=A_UMD_DATA_DETAILS&d-444584-p=1')

# login should be cookied, we try to fetch the page now
while len(pages) > current_page_index:
	req = urllib2.Request('https://www.wireless.att.com' + pages[current_page_index])
	response = opener.open(req)
	data = response.read()
	htmlparser = ATTParser(formatter.NullFormatter())
	htmlparser.feed(data)
	htmlparser.close()

	# this is a fixup, we drop the last row because there is a bogus row that is in the <tbody> (should be in <tfoot>)
	entries.pop()

	# go to next page
	current_page_index += 1

# dump out the entries
for entry in entries:
	print entry.date, entry.time, entry.toFrom, entry.type, entry.direction

