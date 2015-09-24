import requests
import sys
import logging

magic = '\xff\xd8\xff'

def strip_jpeg(jpeg):
	return magic + magic.join(jpeg.split(magic)[1:])


def get(inputurl, outputdir, max_frames):
	max_frames += 2
	boundary = None
	jpegs = []

	req = requests.get(inputurl, stream=True)
	boundary = req.headers['content-type'].split('=')[-1]
	if not boundary.startswith('--'):
		boundary = '--%s' % boundary
	for i, jpeg in enumerate(req.iter_lines(delimiter=boundary)):
		logging.debug('read line %d (%d jpegs)', i, len(jpegs))
		jpegs.append(jpeg)

		if len(jpegs) >= max_frames:
			break

	jpegs = filter(lambda x: x != '' and x != magic, [strip_jpeg(jpeg) for jpeg in jpegs])

	for i, frame in enumerate(jpegs):
		outputfilename = "%s/%s.jpg" % (outputdir, str(i).zfill(5))
		fh = open(outputfilename, 'wb')
		fh.write(frame)
		fh.close()
		logging.debug("Wrote %s", outputfilename)

if __name__ == '__main__':
	inputurl = sys.argv[1]
	outputdir = sys.argv[2]
	frames = int(sys.argv[3]) if len(sys.argv) == 4 else 20
	get(inputurl, outputdir, frames)