import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/ivan/thor/venv/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/ivan/thor/tagteam')
sys.path.append('/home/ivan/thor/tagteam/tagteam')

os.environ['DJANGO_SETTINGS_MODULE'] = 'tagteam.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/ivan/thor/venv/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
