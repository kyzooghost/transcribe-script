# python3 main.py <FILE_PATH>

import boto3
import logging
import os
import sys
import time
from dotenv import load_dotenv
load_dotenv()

# Parse CLI args
if len(sys.argv) == 1:
    print('Did not provide any CLI arguments')
    sys.exit(0)

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
    s3_client.upload_file(recording_path, os.getenv('S3_BUCKET'), f"input-files/{filename}")
    print("Succeeded uploading recording to S3")
except Exception as e:
    print(f"An exception occurred while uploading S3 file: {e}")
    sys.exit(0)

transcribe_client = boto3_session.client('transcribe', os.getenv('AWS_REGION'))

transcription_job_name = recording_path + "-medical-transcription-job"
job_uri = f"s3://{os.getenv('S3_BUCKET')}/input-files/{filename}"

try:
    # https://docs.aws.amazon.com/transcribe/latest/APIReference/API_StartMedicalScribeJob.html
    transcribe_client.start_medical_transcription_job(
        MedicalTranscriptionJobName = transcription_job_name,
        Media = {
          'MediaFileUri': job_uri
        },
        OutputBucketName = os.getenv('S3_BUCKET'),
        LanguageCode = 'en-US',
        Specialty = 'PRIMARYCARE',
        Type = 'CONVERSATION',
        OutputKey = 'output_files/'
    )
    print("Started medical transcription job")
except Exception as e:
    print(f"An exception occurred while doing transcription job: {e}")
    sys.exit(0)

while True:
    status = transcribe_client.get_medical_transcription_job(MedicalTranscriptionJobName = transcription_job_name)
    if status['MedicalTranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)    

print(status)
    