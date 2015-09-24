import requests
import json
from urllib import quote
from StringIO import StringIO
import random
import logging
import util

config = util.get_config()
text_source_csvs = config.get('treasurecolumn', 'text_source_csvs').split()

lines = []
for source in text_source_csvs:
	lines.extend(open(util.get_cur_dir() + '/data/' + source, 'r').readlines())

def retrieve(identifier):
	url = "http://archive.org/details/%s?output=json" % quote(identifier)
	result = requests.get(url)
	try:
		data = result.json()
		return data
	except ValueError:
		return None

def get_text(data):
	for filename, fileobj in data['files'].iteritems():
		if fileobj['format'] == 'DjVuTXT':
			url = "http://%s%s%s" % (data['server'], data['dir'], filename)
			req = requests.get(url)
			return req.content
	return None

def random_text(writefile=None):
	line = random.choice(lines).replace('"', '').strip()
	data = retrieve(line)
	if data is None:
		return None
	txt = get_text(data)
	if txt is None:
		return None
	return txt

if __name__ == '__main__':
	text = random_text()
	logging.debug("Text: %s" % text)