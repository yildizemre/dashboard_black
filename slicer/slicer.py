import cv2
from redis import Redis
import time
import base64
import uuid
import pika
import sys
import numpy as np
import datetime
import sys
import signal
import json 
import os
from dotenv import load_dotenv
from pathlib import Path
import logging
import graypy
# from py_zipkin.zipkin import zipkin_span,zipkin_client_span
# from py_zipkin.transport import BaseTransportHandler 
import random
import requests 
import struct
import datetime
from redis import Redis
# class HttpTransport(BaseTransportHandler):
    
#     def get_max_payload_bytes(self):
#         return None
#     def send(self, encoded_span):
#         print('5')
#         # The collector expects a thrift-encoded list of spans.
#         requests.post(
#             'http://localhost:9411/api/v1/spans',
#             data=encoded_span,
#             headers={'Content-Type': 'application/x-thrift'},
#         )

# some_handler = HttpTransport()

env_path = Path('.') / 'project.env'
load_dotenv(dotenv_path=env_path)


retry = 0
p_uudi = []

log_level = os.getenv('LOG_LEVEL')
graylog_host = os.getenv('GRAYLOG_HOST')
graylog_port = os.getenv('GRAYLOG_PORT')

logger = logging.getLogger()
cap = None

if graylog_host:
    graylog_handler = graypy.GELFUDPHandler(graylog_host, int(graylog_port))
    logger.addHandler(graylog_handler)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(log_level)

def signal_handler(sig, frame):
    global cap
    connection.close()
    cap.release()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# r1=redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    if connection.is_open:
        logger.info('RabbitMQ Connection Complete')
except Exception as error:
    logger.error('Error:', error._class.name_)
    exit(1)



# @zipkin_client_span(service_name='frame', span_name='frameRead')
def frameread(capt):
    
    ret,frame = capt.read()
    return ret,frame


# @zipkin_client_span(service_name='frame', span_name='Capture')
def capt():
    cap = cv2.VideoCapture(os.getenv('RTMP_SERVER'), cv2.CAP_FFMPEG)
    return cap

# @zipkin_client_span(service_name='frame', span_name='reconnect')
def reconnect(retry): 
    global cap
    print("disconnected")
    time.sleep(1)
    cap.release()
    logger.info(os.getenv("RTMP_SERVER"))
    cap = cv2.VideoCapture(os.getenv('RTMP_SERVER'), cv2.CAP_FFMPEG)
    if retry > 5:
        print('tried to connect'+str(retry)+'times')


# @zipkin_client_span(service_name='frame', span_name='Decode')
def decuuid(frame):
    logger.info(frame.shape)
    logger.info(frame.dtype)
    encoded = frame.tobytes()
   
    return encoded
  

# @zipkin_client_span(service_name='frame', span_name='redisandrabbit')
def redisandrabbit(json_data,encode):
    frame_uuid = json_data['frame_uuid']
    redis.set(frame_uuid +'_data', encode , 70)
    json_data=json.dumps(json_data)
    redis.set(frame_uuid, json_data , 70)
    channel.basic_publish(
                            exchange='',
                            routing_key=os.getenv('RABBIT_OUTPUT_QUEUE'),
                            body=json_data,
                            properties=pika.BasicProperties(
                                delivery_mode=2,  # make message persistent
                                expiration="60000",
                        ))
    return True
sayac = 0

while True:
    
        sayac+=1
    #    with zipkin_span(
    #             service_name='slicer',
    #         span_name='frame',
    #         transport_handler=some_handler,
    #         sample_rate=0.05
    #         ): 
    #     logger.debug('OK')
        if sayac== 1 :
            cap =capt()
        else:
            pass
        if cap:
            ret,frame=frameread(cap)
            if not cap.isOpened() or not ret:
                    retry =retry+1
                    reconnect(retry)
                    continue
            retry=0  
            starttime = time.time()
            frame_uuid = str(uuid.uuid4())
            encode = decuuid(frame)
            p_uudi.append(frame_uuid)
            stime= float(starttime-(float(os.getenv('TIMESTAMPT'))))
            y= datetime.datetime.fromtimestamp(stime)
            stime=round(stime,2)
            realtime=(y.strftime('%H:%M:%S'))
            if len(p_uudi)==1:
                json_data = {
                    "captured_at" :  stime,
                    "camera_id" : os.getenv('CAMERA_ID'),
                    "device_id" : os.getenv('DEVICE_ID'),
                    "frame_uuid": p_uudi[0],
                    "previous_frame_uuid" : p_uudi[0]
                }
            if len(p_uudi) >= 2 :
                json_data = {
                    "captured_at" :  stime,
                    "camera_id" : os.getenv('CAMERA_ID'),
                    "device_id" : os.getenv('DEVICE_ID'),
                    "frame_uuid": p_uudi[1],
                    "previous_frame_uuid" : p_uudi[0]
                }
                p_uudi[0]=p_uudi[1]
                del p_uudi[1]
            logger.info(json_data)
            redisandrabbit(json_data,encode)