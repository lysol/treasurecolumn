import convert_mjpeg
import ytupload
import random
import logging
import os
from oauth2client.tools import argparser
import config
import util

config = util.get_config()
tmp_movie_path = config.get('treasurecolumn', 'tmp_movie_path')

def run(url, frames=20, rate=-1, 
	google_secret=os.getcwd() + '/client_secrets.json', 
	google_credentials=os.getcwd() + '/credentials.json'):
	logging.debug("Trying %s", url)
	if url.endswith('.mpg') or url.endswith('.mp4'):
		convert_mjpeg.convert_mp4(url, tmp_movie_path)
	else:
		convert_mjpeg.convert(url, tmp_movie_path, frames, rate)
	ytupload.upload_video(args, tmp_movie_path, google_secret, google_credentials)

if __name__ == '__main__':
	argparser.add_argument("--randomize", action='store_true', default=False)
	argparser.add_argument("--url", "-u", required=False, help="Video URL", default=None)
	argparser.add_argument("--urlsfile", "-U", required=False, help="Video URL File, one per line", default=[])
	argparser.add_argument("--frames", "-f", required=False, type=int, help="Frames", default=2000)
	argparser.add_argument("--rate", "-r", required=False, type=int, help="Rate", default=-1)
	argparser.add_argument("--debug", "-d", action='store_true', default=False)
	argparser.add_argument("--googlesecret", "-s", type=str, default=os.getcwd() + '/client_secrets.json')
	argparser.add_argument("--googlecredentials", "-c", type=str, default=os.getcwd() + '/credentials.json')
	args = argparser.parse_args()
	if args.debug:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.ERROR)

	if args.randomize and random.randint(0,100) > 10:
		exit()
	if args.url is None and len(args.urlsfile) == 0:
		raise Exception("Specifying either --url or --urlsfile is required")
	if args.urlsfile:
		if not os.path.exists(args.urlsfile):
			raise Exception("Couldn't find %s" % args.urlsfile)
		urls = open(args.urlsfile, 'r').readlines()
		url = random.choice(urls).strip()
	else:
		url = args.url
	run(url, args.frames, args.rate, google_secret=args.googlesecret, 
		google_credentials=args.googlecredentials)
