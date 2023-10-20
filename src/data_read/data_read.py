from os import path
import sys, os
import datetime
from json import dumps, loads
from time import sleep
from random import randint
import numpy as np
import requests
from kafka import KafkaConsumer,TopicPartition
import re
import time

    
    
def clean_message(message, ratings_file):
    """
    Extract data from a log entry in a message and write it to a ratings file.
    Args:
        message (str): A log message.
        ratings_file (file): A file object to write ratings data to.
    """
    pattern = r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}),(\d+),GET /rate/(.*?\d{4})=(\d{1})$'
    match = re.search(pattern, message.value)
    
    if match:
        time, userid, movieid, rating = match.groups()
        if int(rating) >= 0 and int(rating) <= 5:
            ratings_file.write(f"{time},{userid},{movieid},{rating}\n")
    

def read_from_broker_hour(consumer, tp, path, hours=24, save_path=None):
    """Read messages from a Kafka broker and extract ratings data to a file."""
    print('Connecting to Kafka broker...')
    
    # Calculate timestamp for 24 hour ago
    timestamp_hrs_ago = int(time.time() - (hours * 60 * 60)) * 1000
    
    if not save_path:
        save_path = path+"kafka_ratings_%d_%dh.csv" %(timestamp_hrs_ago, hours)

    ratings_file = open(save_path, 'w')
    ratings_file.write('time,userid,movieid,rating\n')

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
            clean_message(message, ratings_file)
            if message.timestamp >= timestamp_now:
                ratings_file.close()
                consumer.close()
                return save_path
    ratings_file.close()
    consumer.close()
    return save_path


def read_from_broker_day(consumer, tp, path, today, day_count=1, save_path=None):
    """Read messages from a Kafka broker and extract ratings data to a file."""
    
    print('Connecting to Kafka broker...')
    
    start_day = today - datetime.timedelta(days = day_count)
    end_day = today - datetime.timedelta(days = 1)

    if not save_path:
        save_path = path+'kafka_ratings_%d%02d%02d_%d%02d%02d.csv' %(start_day.year, start_day.month, start_day.day, end_day.year, end_day.month, end_day.day)

    ratings_file = open(save_path, 'w')
    ratings_file.write('time,userid,movieid,rating\n')
    
    # Calculate timestamp
    timestamp_today = today.timestamp() * 1000
    timestamp_start = start_day.timestamp() * 1000
    
    # Use the stored timestamp to seek to the earliest offset for 
    # each partition that corresponds to the data of yesterday.
    offset_24hr_ago = consumer.offsets_for_times({tp: timestamp_start})[tp]
    consumer.seek(tp, offset_24hr_ago.offset)
    
    while True:
        messages = consumer.poll(timeout_ms=4000)
        if not messages:
            break
        for message in messages[tp]:
            clean_message(message, ratings_file)
            if message.timestamp >= timestamp_today:
                ratings_file.close()
                consumer.close()
                return save_path
    ratings_file.close()
    consumer.close()
    return save_path

def main():

    ## when run this file in command line, can use different mode
    # example 1: python3 data_read.py hours 24
    # example 2: python3 data_read.py day
    # example 3: python3 data_read.py day 2023-03-24
    # example 4: python3 data_read.py days 3

    # need to connect to kafka first
    # ssh -o ServerAliveInterval=60 -L 9092:localhost:9092 tunnel@128.2.204.215 -NT

    mode  = sys.argv[1]

    topic= "movielog2"
    save_path = sys.argv[3]

    path = "../../data/data_daily/"
    
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

    # Consume messages starting from the earliest offset until the latest offset.
    if mode == "day":
        if len(sys.argv) > 2:
            day_beginning = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
            final_path = read_from_broker_day(consumer, tp, path, day_beginning)
            print("done reading, mode 3")
        else:
            today_beginning = datetime.datetime.combine(datetime.date.today(), datetime.time()) 
            final_path = read_from_broker_day(consumer, tp, path, today_beginning)
            print("done reading, mode 2")

    if mode == "days":
        today_beginning = datetime.datetime.combine(datetime.date.today(), datetime.time())
        final_path = read_from_broker_day(consumer, tp, path, today_beginning, int(sys.argv[2]), save_path)
        print("done reading, mode 4")

    if mode == "hours":
        print("hereerererer")
        final_path = read_from_broker_hour(consumer, tp, path, int(sys.argv[2]), save_path)
        print("done reading, mode 1")   
    
    print("data file saved at "+final_path)
    #Update the stored timestamp with the current timestamp at the end of the script.
    consumer.close()



if __name__=="__main__":
    main()

