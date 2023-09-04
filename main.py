# python3 main.py <FILE_PATH>

import boto3
import logging
import os
import sys
import time
from dotenv import load_dotenv

# logging.basicConfig(level=logging.DEBUG, filename='sample.log')
# load_dotenv()


# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

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

# try:
#     print("Uploading recording to S3")
#     s3_client.upload_file(recording_path, os.getenv('S3_BUCKET'), f"input-files/{filename}")
#     print("Succeeded uploading recording to S3")
# except Exception as e:
#     print(f"An exception occurred while uploading S3 file: {e}")
#     sys.exit(0)

# 'transcribe' service not HealthScribe? us-east-1 restriction?
# transcribe_client = boto3_session.client('transcribe', os.getenv('AWS_REGION'))
transcribe_client = boto3_session.client('transcribe', os.getenv('us-east-1'))

transcribe_job_name = recording_path + "-medical-scribe-job"
job_uri = f"s3://{os.getenv('S3_BUCKET')}/input-files/{filename}"

# print(transcribe_client)

# logging.debug('transcribe_client: %s', transcribe_client)
print(dir(transcribe_client))
# logging.info("Loging dict ---> {0}".format(transcribe_client))

# try:
#     print("Starting transcribe job")
#     # https://docs.aws.amazon.com/transcribe/latest/APIReference/API_StartMedicalScribeJob.html
#     transcribe_client.start_medical_scribe_job(
#         MedicalScribeJobName = transcribe_job_name,
#         Media = {
#           'MediaFileUri': job_uri
#         },
#         OutputBucketName = os.getenv('S3_BUCKET'),
#         DataAccessRoleArn = os.getenv('DATA_ACCESS_ROLE_ARN'),
#         Settings = {
#           'ShowSpeakerLabels': false,
#           'ChannelIdentification': true
#         },
#         ChannelDefinitions = [
#           {
#             'ChannelId': 0, 
#             'ParticipantRole': 'CLINICIAN'
#           }, {
#             'ChannelId': 1, 
#             'ParticipantRole': 'PATIENT'
#           }
#         ]
#     )
# except Exception as e:
#     print(f"An exception occurred while doing transcribe job: {e}")
#     sys.exit(0)

# while True:
#     status = transcribe.get_medical_scribe_job(MedicalScribeJobName = transcribe_job_name)
#     if status['MedicalScribeJob']['MedicalScribeJobStatus'] in ['COMPLETED', 'FAILED']:
#         break
#     print("Not ready yet...")
#     time.sleep(5)    
# print(status)
    