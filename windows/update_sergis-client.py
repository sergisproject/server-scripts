"""
Script to pull the latest changes from the SerGIS Client git repository and
put them in the web directory.
"""

import os.path, subprocess, shutil
from send2trash.send2trash import send2trash

GIT_REPO = os.path.expanduser("~\\Desktop\\JAKE\\GitHub\\sergis-client")
WEB_DIR = "C:\\inetpub\\wwwroot\\serious_game_spatial_thinking\\web_game"
GITHUB_DIR = os.path.expanduser("~\\AppData\\Local\\GitHub")

GIT_PATH = ""
for f in os.listdir(GITHUB_DIR):
    if f[:12] == "PortableGit_":
        GIT_PATH = GITHUB_DIR + "\\" + f + "\\bin\\git.exe"
        break

if GIT_PATH:
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
