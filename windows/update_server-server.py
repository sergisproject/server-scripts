"""
Script to pull the latest changes from the SerGIS Server git repository and
put them in the web directory.

The defaults here assume IIS with iisnode, but it can be easily modified for a
different environment.

Before running this, make sure to set the configuration.

Usage:

    python2 update_sergis-server.py

      Fully update the server web directory by:
        1. Pull the latest changes in the git repo
        2. Pull the latest changes in the git submodules
        3. Run `npm install` in the git repo directory
        4. Run `grunt dist` in the git repo directory
        5. Set IIS permissions on the web directory.
        6. Clear out the web directory.
        7. Copy from the git repo to the web directory.
        8. Copy config files to the web directory.

    python2 update_sergis-server.py lite

      Update the server web directory with the latest changes from the git repo
      without reinstalling all dependencies.
        1. Pull the latest changes in the git repo
        2. Pull the latest changes in the git submodules
        3. Run `grunt dist` in the git repo directory
        4. Copy from the git repo to the web directory.
        5. Copy config files to the web directory.
"""

import os, os.path, subprocess, shutil, sys


################################################################################
## Configuration
################################################################################


# Whether we are running the "lite" version (see above)
LITE = False
if len(sys.argv) > 1 and sys.argv[1] == "lite":
    LITE = True

# The directory where the sergis-server git repo is
GIT_REPO = os.path.expanduser("~\\Desktop\\JAKE\\GitHub\\sergis-server")

# The submodules in the sergis-server git repo
GIT_SUBMODULES = [
    os.path.join(GIT_REPO, "sergis-client"),
    os.path.join(GIT_REPO, "sergis-author")
]

# The web directory (where we're "publishing" to)
WEB_DIR = "C:\\sergis-server"

# When we're clearing out the web directory, which files/folders to ignore (i.e. keep)
WEB_DIR_CLEAR_IGNORE = ["iisnode"]

# The config.js file for SerGIS Server (to overwrite the repo default)
CONFIG_JS = os.path.expanduser("~\\Desktop\\JAKE\\sergis-server-config.js")

# Config files to copy to the web directory: [(from, to), ...]
CONFIG_FILES = [
    # The node.js server config file
    (CONFIG_JS, os.path.join(WEB_DIR, "config.js")),
    # The iisnode config file (here, it's relative to the script location)
    (os.path.join(os.path.dirname(os.path.realpath(__file__)), "sergis-server-web.config"), os.path.join(WEB_DIR, "web.config"))
]

# Config files requires to run grunt: [(from, to), ...]
GRUNT_CONFIG_FILES = [
    # The node.js server config file
    (CONFIG_JS, os.path.join(GIT_REPO, "config.js"))
]

# Ignored files (to not copy from the repo to the web directory)
GIT_REPO_IGNORE = [".git", "config.js", ".gitignore", ".gitmodules"]

# Additional ignored files if we're running in "lite mode"
GIT_REPO_IGNORE_LITE = ["node_modules"]

# The directory to the nodejs installation
NODE_DIR = "C:\\Program Files\\nodejs"

# The location of the grunt command
GRUNT_LOCATION = os.path.expanduser("~\\AppData\\Roaming\\npm\\grunt.cmd")

# The location of the git executable (this example uses GitHub's git)
GIT_PATH = ""
for f in os.listdir(os.path.expanduser("~\\AppData\\Local\\GitHub")):
    if f[:12] == "PortableGit_":
        GIT_PATH = GITHUB_DIR + "\\" + f + "\\bin\\git.exe"
        break


################################################################################
## Functions for doing different tasks to update the web directory
################################################################################


def updateGitRepos():
    """Update the git repository and any submodules."""
    print "Running", GIT_PATH
    print ""
    print subprocess.check_output([GIT_PATH, "pull"], cwd=GIT_REPO)
    print ""
    for submod in GIT_SUBMODULES:
        print subprocess.check_output([GIT_PATH, "pull"], cwd=submod)
        print ""

def runNPM():
    """Run npm install"""
    print "Running npm install"
    subprocess.check_call([
        os.path.join(NODE_DIR, "node.exe"),
        os.path.join(NODE_DIR, "node_modules", "npm", "bin", "npm-cli.js"),
        "install"
    ], cwd=GIT_REPO)
    print ""

def runGrunt():
    """Run grunt dist"""
    print "Running grunt dist"
    # Firstly, copy in any config files
    for src, dst in GRUNT_CONFIG_FILES:
        if os.path.exists(dst):
            os.rename(dst, dst + ".BAK")
        shutil.copy(src, dst)
    # Run grunt
    subprocess.check_call([
        GRUNT_LOCATION,
        "dist"
    ], cwd=GIT_REPO)
    # Reset any config files that we copied in
    for src, dst in GRUNT_CONFIG_FILES:
        if os.path.exists(dst) and os.path.exists(dst + ".BAK"):
            os.unlink(dst)
            os.rename(dst + ".BAK", dst)
    print ""

def setIISPermissions():
    """Set proper permissions (only needs to be done once)"""
    print "Setting permissions on", WEB_DIR
    subprocess.check_call(["C:\\windows\\system32\\icacls.exe", WEB_DIR, "/grant", "IIS_IUSRS:(OI)(CI)F"])
    print ""

def clearWebDirectory():
    """Clear out the directory"""
    print "Clearing out", WEB_DIR
    for item in os.listdir(WEB_DIR):
        if not item in WEB_DIR_CLEAR_IGNORE:
            file_path = os.path.join(WEB_DIR, item)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    print ""

def copyToWebDirectory():
    """Copy the latest files to the web directory"""
    for item in os.listdir(GIT_REPO):
        if not (item in GIT_REPO_IGNORE or (LITE and item in GIT_REPO_IGNORE_LITE)):
            print "Copying", item
            if os.path.isdir(os.path.join(GIT_REPO, item)):
                if os.path.exists(os.path.join(WEB_DIR, item)):
                    shutil.rmtree(os.path.join(WEB_DIR, item))
                shutil.copytree(os.path.join(GIT_REPO, item), os.path.join(WEB_DIR, item), ignore=shutil.ignore_patterns(*GIT_REPO_IGNORE))
            else:
                if os.path.exists(os.path.join(WEB_DIR, item)):
                    os.remove(os.path.join(WEB_DIR, item))
                shutil.copy(os.path.join(GIT_REPO, item), WEB_DIR)
    print ""

def copyConfigFiles():
    """Copy config files"""
    for src, dst in CONFIG_FILES:
        print "Copying", src, "to", dst
        shutil.copy(src, dst)
    print ""


################################################################################
## Actually run the tasks to update the web directory
################################################################################


# Alrighty, let's get started!
if __name__ == "__main__":
    if not GIT_PATH:
        print "Coultn't find git!"
    else:
        updateGitRepos()
        if not LITE:
            runNPM()
        runGrunt()
        if not LITE:
            setIISPermissions()
            clearWebDirectory()
        copyToWebDirectory()
        copyConfigFiles()

