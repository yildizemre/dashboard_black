import pika
from redis import Redis
import numpy as np
import sys
import signal
import json 
import requests
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import logging
import graypy

import cv2

env_path = Path('.') / 'project1.env'
load_dotenv(dotenv_path=env_path)

log_level = os.getenv('LOG_LEVEL')
graylog_host = os.getenv('GRAYLOG_HOST')
graylog_port = os.getenv('GRAYLOG_PORT')

logger = logging.getLogger()


if graylog_host:
    graylog_handler = graypy.GELFUDPHandler(graylog_host, int(graylog_port))
    logger.addHandler(graylog_handler)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.setLevel(log_level)

# logger.info('Frame_uploader starting')
logger.setLevel(log_level)
logger.info('{} starting'.format(os.getenv('PROJECT_NAME')))

def signal_handler(sig, frame):
    connection.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST')))
channel = connection.channel()
logger.info('ConnectionRabbitMQ')
logger.info('RabbitMQ Queue'+str(os.getenv('RABBIT_ROUTING_KEY')))
redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'),  db=os.getenv('REDIS_DB_PORT'))
logger.info('ConnectionRedis')

def index(ch,properties,method,body):
    
        json_data = json_load(body)       
        redis_data = redis_get(json_data)
        print(json_data)
        if redis_data:           
            original_frame = frame(redis_data)   





            
             
            cv2.imshow('Frame',original_frame)
            cv2.waitKey(1)


        # else:
        #     logger.info("Data Not Found")
        #     ch.basic_ack(delivery_tag=method.delivery_tag)


def json_load(body):
    json_data = body.decode()
    return json.loads(json_data)


def redis_get(json_data):
    if redis.exists(json_data['frame_uuid'] + "_data"):
        return  redis.get(json_data['frame_uuid'] + "_data")
    return False

def frame(redis_data):
    jpg_as_np = np.frombuffer(redis_data, dtype=np.uint8)
    org_frame = jpg_as_np.reshape(720,1280,3)   
    return org_frame

def callback(ch,method, properties, body):
    index(ch,properties,method,body)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=os.getenv('RABBIT_ROUTING_KEY'), on_message_callback=callback,auto_ack=True)
channel.start_consuming()