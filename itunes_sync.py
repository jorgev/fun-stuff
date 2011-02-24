#!/usr/bin/env python
# encoding: utf-8
"""
itunes_sync.py

Created by Jorge Velázquez on 2010-09-18.
Copyright (c) 2010. All rights reserved.
"""

import sys
import getopt
import shutil
import urllib
import urlparse
import os
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
		xml_file = None
		playlist_name = None
		output = None
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-i", "--input"):
				xml_file = value
			if option in ("-p", "--playlist"):
				playlist_name = value
			if option in ("-o", "--output"):
				output = value
		
		# all options are required
		if not xml_file or not playlist_name or not output:
			raise Usage('input, playlist, and output options are all required')
			return 3
			
		# make sure destination dir ends in a slash
		if output[-1] != '/':
			output += '/'
		
		print 'Parsing XML file...'
		doc = minidom.parse(xml_file)
		
		print 'Searching for playlist %s...' % playlist_name
		
		# we start out with the top level dictionary
		plist = get_node(doc.childNodes, 'plist')
		top_dict = get_node(plist.childNodes, 'dict')
		music_folder_node = get_key(top_dict.childNodes, 'Music Folder')
		music_folder = get_text(music_folder_node.childNodes)
		playlists = get_key(top_dict.childNodes, 'Playlists')
		playlist_array = get_array(playlists.childNodes)
		p = None
		for playlist in playlist_array:
			playlists_dict = get_node(playlists.childNodes, 'dict')
			name_node = get_key(playlist.childNodes, 'Name')
			if get_text(name_node.childNodes) == playlist_name:
				p = playlist
				break
		
		# if we didn't find the playlist, not much else to do
		if not p:
			print 'Playlist %s not found' % playlist_name
			return 1
		
		# read in the track IDs from the playlist
		print 'Playlist found, reading track IDs'
		track_dicts = get_node(playlist.childNodes, 'array')
		track_ids = get_track_ids(track_dicts.childNodes)

		# must have at least one track or there is nothing to do
		if len(track_ids) == 0:
			print 'No tracks found in playlist'
			return 1
		
		# now that we have the track IDs, we need to look them up
		print '%d tracks found in playlist, getting info for them now...' % len(track_ids)
		tracks = get_key(top_dict.childNodes, 'Tracks')
		
		# tracks are key/dict pairs
		sync_flag = False
		for node in tracks.childNodes:
			if node.nodeType == node.ELEMENT_NODE and node.nodeName == 'key':
				if get_text(node.childNodes) in track_ids:
					sync_flag = True
			elif node.nodeType == node.ELEMENT_NODE and node.nodeName == 'dict' and sync_flag:
				name_node = get_key(node.childNodes, 'Name')
				artist_node = get_key(node.childNodes, 'Artist')
				location_node = get_key(node.childNodes, 'Location')
				name = get_text(name_node.childNodes)
				artist = get_text(artist_node.childNodes)
				location = get_text(location_node.childNodes)
				if location.find(music_folder) == 0:
					relative_path = urllib.unquote(location[len(music_folder):])
					source = urllib.unquote(urlparse.urlparse(location).path)
					dest = output + relative_path
					target_dir = os.path.split(dest)[0]
					if not os.path.exists(target_dir):
						os.makedirs(target_dir)
					if not os.path.exists(dest):
						print 'Copying \'%s - %s\'...' % (name, artist)
						shutil.copy(source, dest)
					else:
						print 'Skipping \'%s - %s\', already in destination' % (name, artist)
				else:
					print 'Unable to copy files that are not in the music folder: %s - %s' % (name, artist)
				sync_flag = False # clear this flag for the next pass
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2
	except Exception, err:
		print >> sys.stderr, err
		return 3
		
def get_node(nodes, name):
	for node in nodes:
		if node.nodeType == node.ELEMENT_NODE and node.nodeName == name:
			return node
	return None
		
def get_key(nodes, name):
	found = False
	for node in nodes:
		if node.nodeType == node.ELEMENT_NODE and node.nodeName == 'key':
			if get_text(node.childNodes) == name:
				found = True
		elif node.nodeType == node.ELEMENT_NODE and found:
			return node
	return None
	
def get_array(nodes):
	array = []
	for node in nodes:
		if node.nodeType == node.ELEMENT_NODE:
			array.append(node)
	return array
	
def get_text(nodes):
	rc = []
	for node in nodes:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)
	
def get_track_ids(nodes):
	ids = []
	for node in nodes:
		if node.nodeType == node.ELEMENT_NODE and node.nodeName == 'dict':
			for subnode in node.childNodes:
				if subnode.nodeType == subnode.ELEMENT_NODE and subnode.nodeName == 'integer':
					ids.append(get_text(subnode.childNodes))
	return ids

if __name__ == "__main__":
	sys.exit(main())
