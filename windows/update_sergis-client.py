"""
Script to pull the latest changes from the SerGIS Client git repository and
put them in the web directory.
"""

import sys, os.path, subprocess, shutil

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "send2trash"))
from send2trash import send2trash

GIT_REPO = "C:\\sergis stuff\\git\\sergis-client"
WEB_DIR = "C:\\inetpub\\wwwroot\\serious_game_spatial_thinking\\web_game"
GIT_PATH = "C:\\Program Files (x86)\\Git\\bin\\git.exe"

print "Running", GIT_PATH
print ""
print subprocess.check_output([GIT_PATH, "pull"], cwd=GIT_REPO)
print ""

# Back up the web directory
if os.path.exists(WEB_DIR):
    print "Moving", WEB_DIR, "to Recycle Bin"
    send2trash(WEB_DIR)
    print ""

# Copy the latest files to the web directory
print "Copying", GIT_REPO, "to", WEB_DIR
shutil.copytree(GIT_REPO, WEB_DIR, ignore=shutil.ignore_patterns(".git"))
