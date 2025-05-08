Python script to use AWS Transcribe to transcribe an arbitrary audio file

Currently only works as a local script

## Prerequisites
- AWS account
- aws cli on local computer, with valid credentials
- S3 bucket created
- .env file populated will fields shown in .env.example

## Steps

1. Install dependencies in venv - `make install`

2. `python3 main.py sample.mp3` Send audio file to AWS Transcribe, and receive the transcription and summary back

3. Download output JSON from AWS Transcribe

4. `python3 transcribe.py <OUTPUT_JSON_FILEPATH>` Parse AWS Transcribe JSON output into more human-friendly JSON (see `sample/sample-transcribe.txt` for an example)