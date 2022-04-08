from wsgiref.simple_server import make_server
import os
import hashlib
from datetime import datetime
import boto3

def main():
    # Region where the sample will be run
    region = 'us-east-1'
    client = boto3.client('sts')
    credentials = client.get_session_token(DurationSeconds=129600)
    print(credentials['Credentials']['AccessKeyId'])
    
    elastictranscoder = boto3.client('elastictranscoder', 
                          aws_access_key_id=credentials['Credentials']['AccessKeyId'],
                          aws_secret_access_key=credentials['Credentials']['SecretAccessKey'],
                          aws_session_token=credentials['Credentials']['SessionToken'],
                          region_name=region
                          )
    
    # This is the ID of the Elastic Transcoder pipeline that was created when
    # setting up your AWS environment:
    pipeline_id = '1649294842147-nj1bp1'
    
    # This is the name of the input key that you would like to transcode.
    input_key = 'mytam.mp4'
    
    # Presets System preset: Generic 480p 16:9.
    mp4_1080p = '1351620000001-000001'

    #All outputs will have this prefix prepended to their output key.
    output_key_prefix = 'output/'
    # Setup the job input using the provided input key.
    job_input = { 'Key': input_key }
    
    # Setup the job outputs using the presets.
    now = datetime.now() # current date and time
    output_key = now.strftime("%Y%m%d%H%M%S")

    job_outputs = [{
        'Key' : 'Output/' + output_key + '.mp4',
        'PresetId' : mp4_1080p,
        'ThumbnailPattern': '',
    }]

    # Creating the job.
    create_job_request = {
        'PipelineId' : pipeline_id,
        'Input' : job_input,
        'Outputs' : job_outputs
    }
    
    elastictranscoder.create_job(**create_job_request)

    print("OK")

if __name__ == '__main__':
    main()
