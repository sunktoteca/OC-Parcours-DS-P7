# This file contains the WSGI configuration required to serve up your
# web application at http://LaureP7.eu.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#

# +++++++++++ GENERAL DEBUGGING TIPS +++++++++++
# getting imports and sys.path right can be fiddly!
# We've tried to collect some general tips here:
# https://help.pythonanywhere.com/pages/DebuggingImportError



import sys

# add your project directory to the sys.path
project_home = '/home/LaureP7/p7api'
if project_home not in sys.path:
    sys.path.append(project_home)
     #sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
# from flask_app import app as application  # noqa
from flask_app import app
application = app.server

