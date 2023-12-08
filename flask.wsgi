import os, sys

# edit your path below
sys.path.append("./httpdocs/nuit-info");

sys.path.insert(0, os.path.dirname(__file__))
from _init_.py import app as application

# set this to something harder to guess
application.secret_key = 'secret'