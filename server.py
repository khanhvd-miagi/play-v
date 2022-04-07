from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import hashlib

import boto3



# def hello_world(request):
#     # Region where the sample will be run
#     region = 'us-east-1'
#     client = boto3.client('elastictranscoder')
    
#     # This is the ID of the Elastic Transcoder pipeline that was created when
#     # setting up your AWS environment:
#     pipeline_id = 'arn:aws:elastictranscoder:us-east-1:117473609707:pipeline/1649294842147-nj1bp1'
    
#     # This is the name of the input key that you would like to transcode.
#     input_key = '20220406/mytam.mp4'
    
#     # HLS Presets that will be used to create an adaptive bitrate playlist.
#     hls_64k_audio_preset_id = '1351620000001-200071';
#     hls_0400k_preset_id     = '1351620000001-200050';
#     hls_0600k_preset_id     = '1351620000001-200040';
#     hls_1000k_preset_id     = '1351620000001-200030';
#     hls_1500k_preset_id     = '1351620000001-200020';
#     hls_2000k_preset_id     = '1351620000001-200010';
#     # HLS Segment duration that will be targeted.
#     segment_duration = '2'
#     #All outputs will have this prefix prepended to their output key.
#     output_key_prefix = 'output/'
#     # Setup the job input using the provided input key.
#     job_input = { 'Key': input_key }
    
#     # Setup the job outputs using the HLS presets.
#     output_key = hashlib.sha256(input_key.encode('utf-8')).hexdigest()
#     hls_audio = {
#         'Key' : 'hlsAudio/' + output_key,
#         'PresetId' : hls_64k_audio_preset_id,
#         'SegmentDuration' : segment_duration
#     }
#     hls_400k = {
#         'Key' : 'hls0400k/' + output_key,
#         'PresetId' : hls_0400k_preset_id,
#         'SegmentDuration' : segment_duration
#     }
#     hls_600k = {
#         'Key' : 'hls0600k/' + output_key,
#         'PresetId' : hls_0600k_preset_id,
#         'SegmentDuration' : segment_duration
#     }
#     hls_1000k = {
#         'Key' : 'hls1000k/' + output_key,
#         'PresetId' : hls_1000k_preset_id,
#         'SegmentDuration' : segment_duration
#     }
#     hls_1500k = {
#         'Key' : 'hls1500k/' + output_key,
#         'PresetId' : hls_1500k_preset_id,
#         'SegmentDuration' : segment_duration
#     }
#     hls_2000k = {
#         'Key' : 'hls2000k/' + output_key,
#         'PresetId' : hls_2000k_preset_id,
#         'SegmentDuration' : segment_duration
#     }
#     job_outputs = [ hls_audio, hls_400k, hls_600k, hls_1000k, hls_1500k, hls_2000k ]
#     playlist = {
#         'Name' : 'hls_' + output_key,
#         'Format' : 'HLSv3',
#         'OutputKeys' : map(lambda x: x['Key'], job_outputs)
#     }
    
#     # Creating the job.
#     create_job_request = {
#         'pipeline_id' : pipeline_id,
#         'input_name' : job_input,
#         'output_key_prefix' : output_key_prefix + output_key +'/',
#         'outputs' : job_outputs,
#         'playlists' : [ playlist ]
#     }
#     create_job_result=client.create_job(**create_job_request)
#     return Response(create_job_result["Id"])

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT"))
#     with Configurator() as config:
#         config.add_route('hello', '/')
#         config.add_view(hello_world, route_name='hello')
#         app = config.make_wsgi_app()
#     server = make_server('0.0.0.0', port, app)
#     server.serve_forever()
def lambda_handler(event, context):
    
    # Job configuration settings. Set these values before running the script.
    pipeline_id = '1649294842147-nj1bp1'         # ID of an existing Elastic Transcoder pipeline
    input_file = '20220406/mytam.mp4'          # Name of an existing file in the S3 input bucket
    output_file = 'AAA'  # Desired root name of the transcoded output files

    # Other job configuration settings. Optionally change as desired.
    output_file_prefix = 'output/'  # Prefix for all output files
    segment_duration = '2'                                         # Maximum segment duration in seconds

    # Elastic Transcoder presets used to create HLS multi-segment
    # output files in MPEG-TS format
    hls_64k_audio_preset_id = '1351620000001-200071'    # HLS Audio 64kb/second
    hls_0400k_preset_id = '1351620000001-200050'        # HLS 400k
    hls_0600k_preset_id = '1351620000001-200040'        # HLS 600k
    hls_1000k_preset_id = '1351620000001-200030'        # HLS 1M
    hls_1500k_preset_id = '1351620000001-200020'        # HLS 1.5M
    hls_2000k_preset_id = '1351620000001-200010'        # HLS 2M

    # Define the various outputs
    outputs = [
        {
            'Key': 'hlsAudio/' + output_file,
            'PresetId': hls_64k_audio_preset_id,
            'SegmentDuration': segment_duration,
        },
        {
            'Key': 'hls0400k/' + output_file,
            'PresetId': hls_0400k_preset_id,
            'SegmentDuration': segment_duration,
        },
        {
            'Key': 'hls0600k/' + output_file,
            'PresetId': hls_0600k_preset_id,
            'SegmentDuration': segment_duration,
        },
        {
            'Key': 'hls1000k/' + output_file,
            'PresetId': hls_1000k_preset_id,
            'SegmentDuration': segment_duration,
        },
        {
            'Key': 'hls1500k/' + output_file,
            'PresetId': hls_1500k_preset_id,
            'SegmentDuration': segment_duration,
        },
        {
            'Key': 'hls2000k/' + output_file,
            'PresetId': hls_2000k_preset_id,
            'SegmentDuration': segment_duration,
        },
    ]

    # Define the playlist
    playlists = [
        {
            'Name': 'hls_' + output_file,
            'Format': 'HLSv3',
            'OutputKeys': [x['Key'] for x in outputs]
        }
    ]

    # Create an HLS job in Elastic Transcoder
    etc_client = boto3.client('elastictranscoder')
    response = etc_client.create_job(PipelineId=pipeline_id,
                                         Input={'Key': input_file},
                                         Outputs=outputs,
                                         OutputKeyPrefix=output_file_prefix,
                                         Playlists=playlists)

    # Output job ID and exit. Do not wait for the job to finish.
    print(f'Created Amazon Elastic Transcoder HLS job {job_info["Id"]}')