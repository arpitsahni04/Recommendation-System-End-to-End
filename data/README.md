## Folder Structure


- data_archive: 
    - training data in milestone 1, including ratings, movie_info, user_info
    - train_data folder that contains the initial ratings matrix used to train the model

- data_daily: 
    - training data in milestone 2
    - plan to generate new data file everyday, which can be used for training and evaluation
    - rating files only have 4 columns: time, movieid, userid, rating

- stats_daily
    - stats.txt is a dummy file used to load new stats collected for each rating matrix of kafka stream
    - stats.csv is a csv file containing the stats comparing train and new ratings matrix