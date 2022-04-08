from wsgiref.simple_server import make_server

import os
import hashlib

import boto3

def main():
    # Region where the sample will be run
    region = 'us-east-1'
    client = boto3.client('elastictranscoder', 
                          aws_access_key_id='ASIARWWPZA7V6PCGEH4H',
                          aws_secret_access_key='JcwghLVMV8mQIAR6pkmCcwdVfW9eWpiLGVgkn55T',
                          aws_session_token='IQoJb3JpZ2luX2VjEDMaCXVzLWVhc3QtMSJIMEYCIQCt4WrjhHARmkOlggpDDAgQbqLc2BooI0mHcz9RhJX9JgIhAJ24oHgkcw4rJ2bFS9yjF703iNC2VwdAYrawr7icq7WqKtwBCMz//////////wEQABoMMTE3NDczNjA5NzA3IgyxhLe3FkfQEFy6BRQqsAFFG7eLKGfr0y3yIzahN29OgemLqeyeUSwGrp4YZ4Apktbnzn7cCstkpkXQQJKuGca0jKRYDg+aVCirT+8LWb2KuM2hlDTpRShUtwKKPVnFyDBRKrpXVJFSpmMlYUkJsgoy/IV9ZpZ1g0t+aoJ07uE8mkR9Wo6U0kC0giZbLDzVwjQ5bZjCJbMFh4jy3NLpz6vuOncarJepAqJg6+79p3COEmc/oBmUnB6IzR6nS8YVgzDHur6SBjqXAdGptzN7+l6KiXV+iD1cgFVrF7LbySydfTNyrqPH/7S3Cdk2CioLKjzw8GN69jBoYW9HPRc69c6hroDsgXky9J34G6yp4wQqZkMg6Eyxqio5JvyvQfMkxDsjJEpQMNtkQVhXyQxp1MYiZqilTlt6sSyHYsANs/fNX0Mw/vluj5B/pd6Y6fRWSqNxvkg7F/wZoFzTJLssCjk=',
                          region_name=region
                          )
    
    # This is the ID of the Elastic Transcoder pipeline that was created when
    # setting up your AWS environment:
    pipeline_id = '1649294842147-nj1bp1'
    
    # This is the name of the input key that you would like to transcode.
    input_key = 'mytam.mp4'
    
    # Presets System preset: Generic 480p 16:9.
    mp4_480p = '1351620000001-000020'

    #All outputs will have this prefix prepended to their output key.
    output_key_prefix = 'output/'
    # Setup the job input using the provided input key.
    job_input = { 'Key': input_key }
    
    # Setup the job outputs using the presets.
    output_key = hashlib.sha256(input_key.encode('utf-8')).hexdigest()


    mp4_480p = {
        'Key' : 'Output/' + output_key + '.mp4',
        'PresetId' : mp4_480p,
        'ThumbnailPattern': '',
    }
    job_outputs = [ mp4_480p ]

    # Creating the job.
    create_job_request = {
        'PipelineId' : pipeline_id,
        'Input' : job_input,
        'Outputs' : job_outputs,
        # 'OutputKeyPrefix' : output_prefix,
        # 'Playlists' : playlist
    }
    
    client.create_job(**create_job_request)

    print("OK")

if __name__ == '__main__':
    main()
