#!/usr/bin/env python
import glob
import sys
import os
from slackviewer.main import main as slackviewer

downloads = os.environ.get('SLACK_BACKUP_DIR') \
    if os.environ.get('SLACK_BACKUP_DIR') is not None \
    else "." # ~/Downloads

port = os.environ.get('PORT') \
    if os.environ.get('PORT') is not None \
    else 5000
slackviewer_path = '$(which slack-export-viewer)'

files = glob.glob('{}/*export*.zip'.format(downloads))
newest = max(files, key=os.path.getctime)
print(newest)

sys.argv[0] = slackviewer_path
sys.argv.append('-z')
sys.argv.append(newest)
sys.argv.append('-p')
sys.argv.append(port)
sys.argv.append('--no-browser')
slackviewer()
