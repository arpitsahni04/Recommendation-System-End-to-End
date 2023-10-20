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

def test_clean_message(ratings_file):
    message = '2022-03-22T12:00:00,1234,GET /rate/movie1234=4'
    clean_message(message, ratings_file)
    ratings_file.seek(0)
    assert ratings_file.readline() == '2022-03-22T12:00:00,1234,movie1234,4\n'
    
    
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
    

def read_from_broker_last24hrs(consumer,tp):
    """Read messages from a Kafka broker and extract ratings data to a file."""
    print('Connecting to Kafka broker...')
    
    # Calculate timestamp for 24 hour ago
    timestamp_24hr_ago = int(time.time() - (24 * 60 * 60)) * 1000
    
    ratings_file = open('kafka_ratings_%d.csv' %timestamp_24hr_ago, 'w')
    ratings_file.write('time,userid,movieid,rating\n')

    # Use the stored timestamp to seek to the earliest offset for 
    # each partition that corresponds to the last 24 hour of data.
    offset_24hr_ago = consumer.offsets_for_times({tp: timestamp_24hr_ago)[tp]
    consumer.seek(tp, offset_24hr_ago.offset)
    
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
                return
    ratings_file.close()
    consumer.close()


def read_from_broker_day(consumer, tp, today):
    """Read messages from a Kafka broker and extract ratings data to a file."""
    
    print('Connecting to Kafka broker...')
    
    yesterday = today - datetime.timedelta(days = 1)
    
    ratings_file = open('kafka_ratings_%d%02d%02d.csv' %(yesterday.year, yesterday.month, yesterday.day), 'w')
    ratings_file.write('time,userid,movieid,rating\n')
    
    # Calculate timestamp
    timestamp_today = today.timestamp() * 1000
    timestamp_yesterday = yesterday.timestamp() * 1000
    
    # Use the stored timestamp to seek to the earliest offset for 
    # each partition that corresponds to the data of yesterday.
    offset_24hr_ago = consumer.offsets_for_times({tp: timestamp_yesterday})[tp]
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
                return
    ratings_file.close()
    consumer.close()
    


if __name__=="__main__":

    ## when run this file in command line, can use different mode
    # example 1: python3 data_read.py 24hr
    # example 2: python3 data_read.py day
    # example 3: python3 data_read.py day 2023-03-24
    mode = sys.argv[1]
    
    topic= "movielog2"
    
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
            read_from_broker_day(consumer, tp, day_beginning)
        else:
            today_beginning = datetime.datetime.combine(datetime.date.today(), datetime.time()) 
            read_from_broker_day(consumer, tp, today_beginning)

    if mode == "24hr":
        read_from_broker_last24hrs(consumer, tp)
    
    print("done reading")
    
    #Update the stored timestamp with the current timestamp at the end of the script.
    consumer.close()
