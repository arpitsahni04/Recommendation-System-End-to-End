## Folder Structure

- drift_check.py: 
    - performs statistical calculations to check for drift in ratings matrix
    - sends e-mail alerts in case of substantial drift
    - saves daily statistics in csv and txt files
    - parameters are as follows:

```
> python3 drift_check.py <train_ratings_df_path> <new_ratings_df_path> <sender_email_address> <sender_email_password> <recipient_email_address> <stats_txt_path> <stats_csv_path>

# example
> python drift_check.py 'data/data_archive/train_data/train_ratings.csv' 'data/data_daily/kafka_ratings_20230323.csv' 'moulya2skala@gmail.com' 'ictlnahisgvwdfdk' 'aishwara@andrew.cmu.edu' 'data/stats_daily/stats.txt' 'data/stats_daily/stats.csv'

```



