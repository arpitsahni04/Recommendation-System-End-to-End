import calendar
import os
import subprocess
import sys
import time

data_reading_file = "/home/cdgamaro/group-project-s23-the-incredi-codes/src/data_read/data_read.py"
model_training_file = "/home/cdgamaro/group-project-s23-the-incredi-codes/src/models/movierecommender.py"

current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)
kafka_ratings_file = "/home/cdgamaro/group-project-s23-the-incredi-codes/data/data_daily/kafka_ratings_%s.csv" % time_stamp
model_pickle_file = "/home/cdgamaro/group-project-s23-the-incredi-codes/src/models/model_%s.pkl" % time_stamp

print("Data file: ", kafka_ratings_file)
print("Model file: ", model_pickle_file)

result = subprocess.run(["/usr/bin/python3", data_reading_file, "days", "1", kafka_ratings_file], capture_output=True)
if not "done reading" in result.stdout.decode():
    print("Could not read data from kafka; exiting")
    print(result)
    sys.exit()
print("Data written to: ", kafka_ratings_file)

result = subprocess.run(["/usr/bin/python3", model_training_file, kafka_ratings_file, model_pickle_file], capture_output=True)
if not "Model Saved" in result.stdout.decode():
    print("Model not trained successfully; exiting")
    print(result)
    sys.exit()
print("Model saved to: ", model_pickle_file)

result = subprocess.run(["sh", "/home/cdgamaro/group-project-s23-the-incredi-codes/deploy.sh", str(time_stamp)], capture_output=True)
print(result)