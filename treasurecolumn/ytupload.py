#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import httplib
import httplib2
import urllib2
import os
import random
import sys
import time
import math
import logging
import archivetext
import util

config = util.get_config()
wordnik_key = config.get('treasurecolumn', 'wordnik_key')
wordnik_api = config.get('treasurecolumn', 'wordnik_api')

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from wordnik import *

wordnik_client = swagger.ApiClient(wordnik_key, wordnik_api)
corruptors = u'▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟'

def corrupt(in_string, perc=.05):
  num = int(math.ceil(len(in_string) * perc))
  try:
    in_string = unicode(in_string, errors='replace')
  except TypeError:
    pass

  for i in range(num+1):
    rand_i = random.randint(0, len(in_string)-1)
    first_part = in_string[:rand_i]
    second_part = in_string[rand_i+1:]
    new_string = unicode(first_part + random.choice(corruptors) + second_part)
    in_string = new_string
  return new_string

def fwl(str):
  ''' return string as fullwidth latin '''
  def tr(c):
    try:
      c = ord(c)
    except:
      return ''
    if c < 32 or c > 126:
      return ''
    if c == 32:
      return ' '
    return unichr(c + 65248)
  return u''.join([tr(c) for c in str])


class DictO(dict):

  def __getattr__(self, name):
    return self[name]

  def __setattr__(self, name, val):
    self[name] = val


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google Developers Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(secrets_file, credentials_file):
  flow = flow_from_clientsecrets(secrets_file,
    scope=YOUTUBE_UPLOAD_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage(credentials_file)
  credentials = storage.get()

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
  tags = None
  if options['keywords']:
    tags = options['keywords'].split(",")

  body=dict(
    snippet=dict(
      title=options['title'],
      description=options['description'],
      tags=tags,
      categoryId=options['category']
    ),
    status=dict(
      privacyStatus=options['privacyStatus']
    )
  )

  # Call the API's videos.insert method to create and upload the video.
  insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    # The chunksize parameter specifies the size of each chunk of data, in
    # bytes, that will be uploaded at a time. Set a higher value for
    # reliable connections as fewer chunks lead to faster uploads. Set a lower
    # value for better recovery on less reliable connections.
    #
    # Setting "chunksize" equal to -1 in the code below means that the entire
    # file will be uploaded in a single HTTP request. (If the upload fails,
    # it will still be retried where it left off.) This is usually a best
    # practice, but if you're using Python older than 2.6 or if you're
    # running on App Engine, you should set the chunksize to something like
    # 1024 * 1024 (1 megabyte).
    media_body=MediaFileUpload(options['file'], chunksize=-1, resumable=True)
  )

  resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      logging.debug("Uploading file...")
      status, response = insert_request.next_chunk()
      if 'id' in response:
        logging.debug("Video id '%s' was successfully uploaded.", response['id'])
      else:
        exit("The upload failed with an unexpected response: %s" % response)
    except HttpError, e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS, e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      logging.error(error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      logging.debug("Sleeping %f seconds and then retrying...", sleep_seconds)
      time.sleep(sleep_seconds)


def upload_video(argparsed, filename, secret_file, credentials_file):
  try:
      word_api = WordsApi.WordsApi(wordnik_client)
      random_words = word_api.getRandomWords(includePartOfSpeech='noun', limit=1)
      if random_words is not None:
          word = random_words[0].word
      else:
          word = '---------------'
  except urllib2.URLError:
      word = '---------------'

  description = None
  while description is None:
    description = archivetext.random_text()
  desclen = random.randint(100,200)
  slice_start = random.randint(0,len(description) - desclen)
  videsc = description[slice_start:slice_start + desclen]
  try:
    logging.debug("Video desc:\n%s", videsc)
  except UnicodeEncodeError:
    logging.debug("Couldn't show description because of encoding")

  args = {
    'category': '22',
    'privacyStatus': 'public',
    'file': filename,
    'title': corrupt(fwl(word.upper())),
    'keywords': '',
    'description': videsc
  }

  youtube = get_authenticated_service(secret_file, credentials_file)

  try:
    initialize_upload(youtube, args)
  except HttpError, e:
    loging.debug("An HTTP error %d occurred:\n%s", (e.resp.status, e.content))

