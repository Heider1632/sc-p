#!/usr/bin/python
activate_this = '/var/www/html/sc-p/app/env/bin/activate_this.py'
with open(activate_this) as f:
	exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/sc-p/')

from app import app as application
application.secret_key='sc-p'
