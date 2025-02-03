# python3 main.py <FILE_PATH>

import boto3
import logging
import os
import sys
import time
from datetime import datetime
import hashlib
from dotenv import load_dotenv
load_dotenv()

# Parse CLI args
if len(sys.argv) == 1:
    print('Did not provide any CLI arguments')
    sys.exit(0)

media_format = "mp3"
max_speaker_count = 10

# Confirm recording file exists  
recording_path = sys.argv[1]
filename = recording_path.split("/")[-1]

if os.path.exists(recording_path) == False:
    print('Recording file does not exist')
    sys.exit(0)

# Upload file to S3 Bucket
boto3_session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'))
s3_client = boto3_session.client('s3', os.getenv('AWS_REGION'))

try:
    print("Uploading recording to S3")
    s3_client.upload_file(recording_path, os.getenv('S3_BUCKET'), f"transcription-input-files/{filename}")
    print("Succeeded uploading recording to S3")
except Exception as e:
    print(f"An exception occurred while uploading S3 file: {e}")
    sys.exit(0)

transcribe_client = boto3_session.client('transcribe', os.getenv('AWS_REGION'))

# Add hash of time to avoid name collision when uploading the same file
transcription_job_name = recording_path + hashlib.sha256(datetime.now().isoformat().encode()).hexdigest()
job_uri = f"s3://{os.getenv('S3_BUCKET')}/transcription-input-files/{filename}"

# https://docs.aws.amazon.com/transcribe/latest/dg/example_transcribe_StartTranscriptionJob_section.html
# https://docs.aws.amazon.com/transcribe/latest/APIReference/API_StartTranscriptionJob.html
try:
    job = transcribe_client.start_transcription_job(
        TranscriptionJobName = transcription_job_name,
        Media = {
          'MediaFileUri': job_uri
        },
        MediaFormat = media_format,
        LanguageCode = 'en-US',
        OutputBucketName = os.getenv('S3_BUCKET'),
        OutputKey = "transcribe-output",
        Settings = {
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 2
        }
    )
    print(f"Started transcription job - {job}")
except Exception as e:
    print(f"An exception occurred while doing transcription job: {e}")
    sys.exit(0)

# https://docs.aws.amazon.com/transcribe/latest/dg/example_transcribe_GetTranscriptionJob_section.html
while True:
    status = transcribe_client.get_transcription_job(TranscriptionJobName = transcription_job_name)
    # print(status)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)

print(status['TranscriptionJob']['Transcript'])