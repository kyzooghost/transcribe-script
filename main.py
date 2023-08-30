import boto3
import logging
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# Parse CLI args
if len(sys.argv) == 1:
    print('Did not provide any CLI arguments')
    sys.exit(0)

# Confirm recording file exists  
recording_path = sys.argv[1]

if os.path.exists(recording_path) == False:
    print('Recording file does not exist')
    sys.exit(0)

# 'transcribe' service not HealthScribe? us-east-1 restriction?
transcribe_client = boto3.Session(profile_name='default').client('transcribe', 'ap-southeast-2')
transcribe_job_name = recording_path + "-medical-scribe-job"
# job_uri = "s3://DOC-EXAMPLE-BUCKET/my-input-files/my-media-file.flac"
# transcribe.start_medical_scribe_job(
#     MedicalScribeJobName = transcribe_job_name,
#     Media = {
#       'MediaFileUri': job_uri
#     },
#     OutputBucketName = 'DOC-EXAMPLE-BUCKET',
#     DataAccessRoleArn = 'arn:aws:iam::111122223333:role/ExampleRole',
#     Settings = {
#       'ShowSpeakerLabels': false,
#       'ChannelIdentification': true
#     },
#     ChannelDefinitions = [
#       {
#         'ChannelId': 0, 
#         'ParticipantRole': 'CLINICIAN'
#       }, {
#         'ChannelId': 1, 
#         'ParticipantRole': 'PATIENT'
#       }
#     ]
# )
# while True:
#     status = transcribe.get_medical_scribe_job(MedicalScribeJobName = transcribe_job_name)
#     if status['MedicalScribeJob']['MedicalScribeJobStatus'] in ['COMPLETED', 'FAILED']:
#         break
#     print("Not ready yet...")
#     time.sleep(5)    
# print(status)
    