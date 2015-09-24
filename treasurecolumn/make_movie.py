import os
import sys
import subprocess
import logging
import archive
from time import sleep
import util

config = util.get_config()
bash_path = config.get('treasurecolumn', 'bash_path')
filter_shell_script = config.get('treasurecolumn', 'filter_shell_script')
tmp_mp3 = config.get('treasurecolumn', 'tmp_mp3')
tmp_processed_mp3 = config.get('treasurecolumn', 'tmp_processed_mp3')
audio_filter_schell_script = config.get('treasurecolumn', 'audio_filter_schell_script')
ffmpeg_location = config.get('treasurecolumn', 'ffmpeg_location')

def make_movie(input_dir, output_file, frame_count, rate=5):
	files = map(lambda f: input_dir + '/' + f, 
		filter(lambda f: f.endswith('.jpg'), os.listdir(input_dir)))

	queue = []
	done = 0

	for i, jpg in enumerate(files):
		parts = os.path.split(jpg)
		num = parts[1].split('.')[0]
		newfilename = os.path.join(parts[0], 'processed_%s.jpg' % num.zfill(5))
		phase = 'diag4' if i % 2 else 'diag42'
		p = subprocess.Popen([bash_path, filter_shell_script, jpg, newfilename, phase, '&'])
		queue.append(p)
		p.communicate()
		while True:
			if len(queue) < 20:
				break
			for proc in queue:
				if proc.poll() is not None:
					queue.remove(proc)
					done += 1
			if (done % 25 == 0):
				logging.debug("Done: %d", done)

	while len(queue) > 0:
		for proc in queue:
			if proc.poll() is not None:
				queue.remove(proc)
				done += 1
			if (done % 25 == 0):
				logging.debug("Done: %d", done)

	max_length = int(frame_count / rate)
	
	realfilename = archive.random_mp3(tmp_mp3)
	if realfilename is not None:
                cmd = [bash_path,
                	   audio_filter_schell_script, 
		               tmp_mp3, tmp_processed_mp3, str(max_length)]
		subprocess.call(cmd)

	logging.debug("Max length is %d", max_length)

	cmd = [ffmpeg_location,
		'-i', '%s/processed_%%05d.jpg' % input_dir, 
		'-i', tmp_processed_mp3,
		'-c:a', 'aac', '-strict', 'experimental', '-map', '0:v:0', '-map', '1:a:0',
		'-vf', 'scale=640:428',
		'-t', str(max_length),
		'-threads', '2', '-r', str(rate), '-vframes', str(frame_count), '-y', 
		'-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-shortest',
		output_file
		]
        logging.debug("Cmd is: %s" % str(cmd))
	subprocess.call(cmd)

if __name__ == '__main__':
	input_dir = sys.argv[1]
	output_file = sys.argv[2]
	frame_count = sys.argv[3]
	make_movie(input_dir, output_file, frame_count)
