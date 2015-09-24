import requests
import json
from urllib import quote
from StringIO import StringIO
import random
import logging
import config
import util

config = util.get_config()
audio_source_csvs = config.get('treasurecolumn', 'audio_source_csvs').split()

lines = []
for source in audio_source_csvs:
	lines.extend(open(util.get_cur_dir() + '/data/' + source, 'r').readlines())

def retrieve(identifier):
	url = "http://archive.org/details/%s?output=json" % quote(identifier)
	result = requests.get(url)
	try:
		data = result.json()
		return data
	except ValueError:
		return None

def get_mp3(data):
	for filename, audiofile in data['files'].iteritems():
		if audiofile['format'] == 'VBR MP3':
			url = "http://%s%s%s" % (data['server'], data['dir'], filename)
			req = requests.get(url)
			return req.content
	return None

def random_mp3(writefile=None):
	line = random.choice(lines).replace('"', '').strip()
	data = retrieve(line)
	if data is None:
		return None
	mp3 = get_mp3(data)
	if mp3 is None:
		return None
	filename = "%s.mp3" % line
	if writefile is None:
		writefile = filename
	oh = open(writefile, 'wb')
	oh.write(mp3)
	oh.close()
	return filename

if __name__ == '__main__':
	filename = random_mp3()
	logging.debug("Saved %s", filename)