#! /usr/bin/python3.6

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '..') #location of wsgi file. e.g. Users/../moodtracker/moodtracker
from views import app as application
application.secret_key = 'anything you wish'
