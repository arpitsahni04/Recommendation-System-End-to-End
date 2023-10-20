import os
import pytest
import pandas as pd
from src.drift_evaluation.drift_check import check_drift


def test_check_drift():
    # Set up test inputs
    train_ratings_df_path = 'data/data_archive/train_data/train_ratings.csv'
    new_ratings_df_path = 'data/data_daily/kafka_ratings_20230323.csv'
    sender_email_address = 'moulya2skala@gmail.com'
    sender_email_password = 'ictlnahisgvwdfdk'
    recipient_email_address = 'aishwara@andrew.cmu.edu'
    stats_txt_path = 'data/stats_daily/stats.txt'
    stats_csv_path = 'data/stats_daily/stats.csv'

    # Call check_drift() function with test inputs
    check_drift(train_ratings_df_path, new_ratings_df_path, sender_email_address,
                sender_email_password, recipient_email_address, stats_txt_path, stats_csv_path)

    # Check if the stats.txt and stats.csv files were created
    assert os.path.isfile(stats_txt_path) == True
    assert os.path.isfile(stats_csv_path) == True

    # Check if the stats.csv file contains the expected columns
    expected_columns = ['Unnamed: 0','Day', 'Train mean', 'New mean', 'Train std', 'New std', 't-statistic', 'p-value']
    stats = pd.read_csv(stats_csv_path)
    assert list(stats.columns) == expected_columns

    