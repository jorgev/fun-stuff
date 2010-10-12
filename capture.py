#!/usr/bin/env python

import sys
import uuid
from boto.gs.connection import GSConnection
from boto.gs.key import Key

# replace with your bucket name
BUCKET_NAME = 'capture.jorgev.com'

def main(argv=None):
	if argv is None:
		argv = sys.argv

	# we expect the file name to be passed in on the command line
	if len(argv) < 2:
		print 'No filename provided'
		return

	# arg should be filename
	filename = argv[1]

	# get the bucket for our upload
	conn = GSConnection()
	bucket = conn.get_bucket(BUCKET_NAME)

	# create a new key with a unique name
	key = Key(bucket)
	key.key = uuid.uuid4().hex
	key.set_contents_from_filename(filename)
	key.make_public()

	# give the user a url good for one hour
	print 'http://%s/%s' % (BUCKET_NAME, key.name)

if __name__ == '__main__':
	sys.exit(main())

