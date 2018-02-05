#!/usr/bin/env python
import glob
import sys
import os
from slackviewer.main import main as slackviewer
import boto3
import botocore

# Get latest backup zip file from s3
s3 = boto3.resource('s3')

bucket_name = os.environ['BUCKET_NAME']
backup_filename = 'backup.zip'

filenames = []
for objects in s3.Bucket(bucket_name).objects.filter():
    filenames.append({'last_modified': objects.last_modified, 'key': objects.key})

newest_s3_filename = max(filenames, key=lambda x: x['last_modified'])

try:
    s3.Bucket(bucket_name).download_file(newest_s3_filename['key'], backup_filename)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise

# Set up slack-export-viewer server
port = os.environ.get('PORT') \
    if os.environ.get('PORT') is not None \
    else 5000
slackviewer_path = '$(which slack-export-viewer)'

sys.argv[0] = slackviewer_path
sys.argv.append('-z')
sys.argv.append(backup_filename)
sys.argv.append('-p')
sys.argv.append(port)
sys.argv.append('--no-browser')
sys.argv.append('--ip')
sys.argv.append('0.0.0.0')
slackviewer()
