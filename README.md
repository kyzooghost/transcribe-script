Python script to use AWS Transcribe to transcribe an arbitrary audio file

## Prerequisites
- AWS account
- S3 bucket created

## Steps

1. Install dependencies in venv - `make install`

2. `python3 main sample.mp3` Send audio file to AWS Transcribe, and receive the transcription and summary back

3. Download output JSON from AWS Transcribe

4. `python3 transcribe.py <OUTPUT_JSON_FILEPATH>` Parse AWS Transcribe JSON output into more human-friendly JSON (see `sample/sample-transcribe.txt` for an example)