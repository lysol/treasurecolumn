import subprocess
import sys
import os
import get_mjpeg
import make_movie
import shutil
import datetime
import util

config = util.get_config()
tmp_dir = config.get('treasurecolumn', 'tmp_dir')
ffmpeg_location = config.get('treasurecolumn', 'ffmpeg_location')

def convert_mp4(input_file, output_file):
	if os.path.exists(tmp_dir):
		shutil.rmtree(tmp_dir)	
	os.mkdir(tmp_dir)

	cmd = [ffmpeg_location,
		'-i', input_file,
		'-threads', '2', '-y', 
		'%s/%%05d.jpg' % tmp_dir
		]
	subprocess.call(cmd)
	make_movie.make_movie(tmp_dir, output_file, 99999, 30)

def convert(input_url, output_file, max_frames, rate=-1):
	if os.path.exists(tmp_dir):
		shutil.rmtree(tmp_dir)
	os.mkdir(tmp_dir)
	start = datetime.datetime.now()
	get_mjpeg.get(input_url, tmp_dir, max_frames)
	end = datetime.datetime.now()
	delta = end - start
	if rate == -1:
		rate = int(max_frames / delta.total_seconds())
	make_movie.make_movie(tmp_dir, output_file, max_frames, rate)

if __name__ == '__main__':
	input_url = sys.argv[1]
	output_file = sys.argv[2]
	max_frames = int(sys.argv[3]) if len(sys.argv) >= 4 else 100
	convert(input_url, output_file, max_frames)