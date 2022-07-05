#!/usr/bin/python
import sys
sys.path.insert(0, '/var/www/html/sc-p/')
from app import app as application
application.secret_key='sc-p'