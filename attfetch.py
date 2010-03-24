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

# this is our class to parse the HTML
class ATTParser(htmllib.HTMLParser):
	def __init__(self, formatter):
		self.table_name = None
		htmllib.HTMLParser.__init__(self, formatter)

	def start_table(self, attributes):
		for attribute in attributes:
			if attribute[0] == 'id':
				self.table_name = attribute[1]
				print self.table_name

	def end_table(self):
		self.table_name = None

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
params = urllib.urlencode({ 'reportActionEvent': 'A_LGN_LOGIN_SUB', 'loginType': 'WIRELESS', 'actionEvent': 'preAuthenticate', 'ajaxSupported': '', 'domain': '.att.com', 'wireless_num': phone, 'pass': password, 'rememberCtn': ''  })
req = urllib2.Request('https://www.wireless.att.com//olam/loginAction.doview', params)

# connect to att login page
response = opener.open(req)

# login should be cookied, we try to fetch the page now
req = urllib2.Request('https://www.wireless.att.com/olam/gotoDataDetailsAction.olamexecute?reportActionEvent=A_UMD_DATA_DETAILS')
response = opener.open(req)
htmlparser = ATTParser(formatter.NullFormatter())
htmlparser.feed(response.read())
htmlparser.close()

