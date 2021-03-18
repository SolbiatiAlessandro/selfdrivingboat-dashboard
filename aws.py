import boto3
import os

def get_last_image(output_path):
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    if not AWS_ACCESS_KEY_ID:
        with open('aws_access_key_id.secret','r') as f:
            AWS_ACCESS_KEY_ID = f.read()
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    if not AWS_SECRET_ACCESS_KEY:
        with open('aws_secret_access_key.secret','r') as f:
            AWS_SECRET_ACCESS_KEY = f.read()
    session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3_client = session.client('s3')
    S3_BUCKET = os.environ.get('S3_BUCKET')
    if not S3_BUCKET:
      S3_BUCKET = 'selfdrivingboatpics'
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
    _all = response['Contents']        
    latest = max(_all, key=lambda x: x['LastModified'])
    print(latest)

    s3_client.download_file(S3_BUCKET, latest['Key'], output_path)

if __name__ == "__main__":
    get_last_image()