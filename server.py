from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import hashlib

import boto3

def hello_world(request):
    # Region where the sample will be run
    region = 'us-east-1'
    client = boto3.client('elastictranscoder', 
                          aws_access_key_id='ASIARWWPZA7V2NFL5KO5',
                          aws_secret_access_key='YQ7qVDBgR3LmUYKpV1Bki3I2Hrc/8p4FRsC1zo4X',
                          aws_session_token='IQoJb3JpZ2luX2VjEDIaCXVzLWVhc3QtMSJIMEYCIQDkTq4Q63srKH1MEX0RvFXsaWldFTsCqSLIw6aXqClAHwIhAPyVC6rhccPJSvhWAe79V+mTfSKr9boVK0Of+G1iOqCqKtwBCMv//////////wEQABoMMTE3NDczNjA5NzA3Igw9QqVi7iGz9oToKJAqsAGnOuPDmQ+izQjCtY/hnxbtA2pJ2MHu+I51PzUOYlTIUIW7d3ps9x16cvV1rsc3zk+H6EunE69T16dMV6x+oC89dLDdRcvycWLd55EsB3Kk/78K1u6stnreKAxAwXD2fW5KmX1Od21CoxmdRm/3nJqzaLRigW1BWyoX8Zmq45aqwA/PYobho7QJlXva/A3h9DAzp8yHiY946nEY2U4selywYX0KORvjjMD8gpXyEN8tQDCenb6SBjqXAW7Oei2tad2ShZ/kWkPeqUvOuA6l+pXMkV7Ew7TH8ygJ+YWy7WxMxXhpnRQi4B7w2EMYq9wKqwTtKau+U9quB/3xiIWxByflcUtyLsk7jaXrdxRSHGwP4RpSSNfsjt2L46HYLDO7nX/e0wFezVn6dTthrE6eAeBzSlufWbvDcVOV72PZM9vj/0ptYQ7xoLuWVA3u55ke5mA=',
                          region_name=region
                          )
    
    # This is the ID of the Elastic Transcoder pipeline that was created when
    # setting up your AWS environment:
    pipeline_id = '1649294842147-nj1bp1'
    
    # This is the name of the input key that you would like to transcode.
    input_key = 'mytam.mp4'
    
    # HLS Presets that will be used to create an adaptive bitrate playlist.
    hls_1000k_preset_id     = '1351620000001-200030';
    hls_1500k_preset_id     = '1351620000001-200020';
    hls_2000k_preset_id     = '1351620000001-200010';
    mp4_480p = '"1351620000001-000020" '
    # HLS Segment duration that will be targeted.
    segment_duration = '60'
    #All outputs will have this prefix prepended to their output key.
    output_key_prefix = 'output/'
    # Setup the job input using the provided input key.
    job_input = { 'Key': input_key }
    
    # Setup the job outputs using the HLS presets.
    output_key = hashlib.sha256(input_key.encode('utf-8')).hexdigest()

    hls_1000k = {
        'Key' : 'hls1000k/' + output_key,
        'PresetId' : hls_1000k_preset_id,
        'ThumbnailPattern': 'hls1000k/thumbnail/' + output_key + '-{resolution}-{count}',
        'SegmentDuration' : segment_duration
    }
    hls_1500k = {
        'Key' : 'hls1500k/' + output_key,
        'PresetId' : hls_1500k_preset_id,
        'ThumbnailPattern': 'hls1500k/thumbnail/' + output_key + '-{resolution}-{count}',
        'SegmentDuration' : segment_duration
    }
    hls_2000k = {
        'Key' : 'hls2000k/' + output_key,
        'PresetId' : hls_2000k_preset_id,
        'ThumbnailPattern': 'hls2000k/thumbnail/' + output_key + '-{resolution}-{count}',
        'SegmentDuration' : segment_duration
    }
    mp4_480p = {
        'Key' : 'mp4/' + output_key,
        'PresetId' : mp4_480p,
        'ThumbnailPattern': ''
    }
    job_outputs = [ hls_1000k, hls_1500k, hls_2000k, mp4_480p ]
    playlist = [
        {
            'Name' : 'hls_' + output_key,
            'Format' : 'HLSv3',
            'OutputKeys' : [
                hls_1000k['Key'], hls_1500k['Key'], hls_2000k['Key'], mp4_480p['Key']
            ]
        }
    ]
    
    # Creating the job.
    
    output_prefix = output_key_prefix + output_key + '/'
    create_job_request = {
        'PipelineId' : pipeline_id,
        'Input' : job_input,
        'Outputs' : job_outputs,
        'OutputKeyPrefix' : output_prefix,
        'Playlists' : playlist
    }
    
    client.create_job(**create_job_request)
    # jobs = client.list_jobs_by_pipeline(PipelineId=pipeline_id)

    return Response("OK")

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
