import datetime
import pytest
import unittest
from unittest.mock import MagicMock, Mock, patch
import time 
# from src.data_read.data_read import clean_message, read_from_broker_last24hrs, read_from_broker_day
from datetime import datetime, timedelta
import tempfile
import os
import io
from contextlib import redirect_stdout

from src.data_read import data_read

def test_clean_message_valid():
    mock_ratings_file = MagicMock()
    message = MagicMock()
    message.value = "2023-03-25T12:00:00,1234,GET /rate/movie1234=3"
    data_read.clean_message(message, mock_ratings_file)
    mock_ratings_file.write.assert_called_once_with("2023-03-25T12:00:00,1234,movie1234,3\n")


@patch.object(data_read, "clean_message") 
def test_read_from_broker_day(mock_clean_message):
    consumer = MagicMock()
    consumer.offsets_for_times.return_value = MagicMock(offset=1)
    consumer.seek.return_value = 0
    message = MagicMock(timestamp=int(time.time()) * 1000)
    consumer.poll.return_value = {"movielog2": [message]}
    consumer.close.return_value = None
    
    day = datetime(2023,3,25)
    data_read.read_from_broker_day(consumer, "movielog2", day)
    
    save_path = data_read.read_from_broker_day(consumer, "movielog2", day)
    assert os.path.exists(save_path)
    os.remove(save_path)


@patch.object(data_read, "clean_message")  
def test_read_from_broker_last24hrs(mock_clean_message):
    consumer = MagicMock()
    consumer.offsets_for_times.return_value = MagicMock(offset=1)
    consumer.seek.return_value = 0
    message = MagicMock(timestamp=int(time.time()) * 1000)
    consumer.poll.return_value = {"movielog2": [message]}
    consumer.close.return_value = None
        
    save_path = data_read.read_from_broker_last24hrs(consumer, "movielog2")
    assert os.path.exists(save_path)
    os.remove(save_path)
    

@patch.object(data_read, "KafkaConsumer")  
@patch.object(data_read, "read_from_broker_last24hrs")  
@patch.object(data_read, "read_from_broker_day")      
def test_main(mock_read_from_broker_day, mock_read_from_broker_last24hrs, mock_KafkaConsumer):
    consumer = MagicMock()
    consumer.assign.return_value = None
    consumer.close.return_value = None
    mock_KafkaConsumer.return_value = consumer
     
    with patch.object(data_read.sys, "argv", ["script.py", "24hr"]):
        f = io.StringIO()
        with redirect_stdout(f):
            data_read.main()
        res = f.getvalue()
        ref = "done reading, mode 1\n"

        assert ref == res
        
    with patch.object(data_read.sys, "argv", ["script.py", "day"]):
        f = io.StringIO()
        with redirect_stdout(f):
            data_read.main()
        res = f.getvalue()
        ref = "done reading, mode 2\n"
        assert ref == res

    with patch.object(data_read.sys, "argv", ["script.py", "day", "2023-03-24"]):
        f = io.StringIO()
        with redirect_stdout(f):
            data_read.main()
        res = f.getvalue()
        ref = "done reading, mode 3\n"
        assert ref == res