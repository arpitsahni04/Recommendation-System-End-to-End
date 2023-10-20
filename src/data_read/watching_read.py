from os import path
import sys, os
import datetime
from time import sleep
import numpy as np
import requests
from kafka import KafkaConsumer,TopicPartition
import re
import time

def clean_message(message, watching_file):
    """
    Extract data from a log entry in a message and write it to a watching records file.
    Args:
        message (str): A log message.
        ratings_file (file): A file object to write ratings data to.
    """
    pattern = r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}),(\d+),GET /data/m/.*\.mpg$'
    match = re.search(pattern, message.value)
    
    if match:
        time, userid = match.groups()
        watching_file.write(f"{time},{userid}\n")
    

def read_from_broker_hour(consumer, tp, save_path, hours=24):
    """Read messages from a Kafka broker and extract ratings data to a file."""
    print('Connecting to Kafka broker...')
    
    # Calculate timestamp for n hour ago
    timestamp_hrs_ago = int(time.time() - (hours * 60 * 60)) * 1000
    
    # save_path = path+"kafka_watching_%d_%dh.csv" %(timestamp_hrs_ago, hours)
    file = open(save_path, 'w')
    file.write('time,userid\n')

    # Use the stored timestamp to seek to the earliest offset for 
    # each partition that corresponds to the last 24 hour of data.
    offset_hrs_ago = consumer.offsets_for_times({tp: timestamp_hrs_ago})[tp]
    consumer.seek(tp, offset_hrs_ago.offset)
    
    # Set the end timestamp to the current time.
    timestamp_now = int(time.time()) * 1000
    
    while True:
        messages = consumer.poll(timeout_ms=4000)
        if not messages:
            break
        for message in messages[tp]:
            clean_message(message, file)
            if message.timestamp >= timestamp_now:
                file.close()
                consumer.close()
                return save_path
    file.close()
    consumer.close()
    return save_path


def main():
    # python3 watching_read.py 10 save_path
    
    hrs = int(sys.argv[1])
    save_path = sys.argv[2]

    topic = "movielog2"
    
    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id='group2',
        value_deserializer = lambda x:x.decode("utf-8"),
        enable_auto_commit=True, 
        auto_commit_interval_ms=800
    )
    
    tp = TopicPartition(topic, 0)
    consumer.assign([tp])

    final_path = read_from_broker_hour(consumer, tp, save_path, hrs)

    consumer.close()