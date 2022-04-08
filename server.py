from wsgiref.simple_server import make_server
import os
import hashlib
from datetime import datetime
import boto3

def main():
    # Region where the sample will be run
    region = 'us-east-1'
    client = boto3.client('elastictranscoder', 
                          aws_access_key_id='ASIARWWPZA7VSRLON3HK',
                          aws_secret_access_key='Iw3ScfgGDOZmXCm3Gbg9zFwPe0+H4SM4/LIto4+s',
                          aws_session_token='IQoJb3JpZ2luX2VjEDMaCXVzLWVhc3QtMSJHMEUCIQDjwWwOzS33bSqLUMYw0mVHU8VYCHBuEU1xbUVgquHbswIgcDwxqazBSz4Y4ZJvj0CXc6ia/jy3NGoU4Wla0G1cxWoq3AEIzP//////////ARAAGgwxMTc0NzM2MDk3MDciDD4AAF+7KhDY/he0lSqwAR+F9C8l3qlxPObHv+E7SSBNO5ou+9lZud1E9O8aBJuC2byOvIjCL+K0Ux4P5sXPpKSIKq2CFFhxgsv9Mi8BTETBYf6YchywcliYwBSyAVRNFvQ3LxivYb1mIWtbD96gqIcmRwqYQcb2MxQOR2Btia7U4epSGHDn/zSns0482TS57iUcftrfmMu5bXPFsiMJzHYMihH737bHw60ATERNrUnmj7DHOQWbIvrMrgUJQ9uYMO7JvpIGOpgBZ/avq2PyqwQFGQSq1QdlPe67kPqKNwJYASbsnMCgUbK5dIIrWQy8U6gSZYHX5BH0tSvmQJQcj9DqGUqTVqMhCw0rXXtjAKTe+GnFTRbHz/f2oBHioBrAZu07CkWxOQSsnx6JdoQ2fPkCsFRHv6NBerbWE70G3h9WS1bW0Yan14NGOanTtKbX+bZZUVZbNgQCsuxXqKX2GkU=',
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
    
    client.create_job(**create_job_request)

    print("OK")

if __name__ == '__main__':
    main()
