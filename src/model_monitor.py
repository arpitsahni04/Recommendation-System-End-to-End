import calendar
import os
import subprocess
import sys
import time

rating_reading_file = "/home/cdgamaro/group-project-s23-the-incredi-codes/src/data_read/data_read.py"
recommend_reading_file = "/home/cdgamaro/group-project-s23-the-incredi-codes/src/data_read/recommend_read.py"
monitor_file = "/home/cdgamaro/group-project-s23-the-incredi-codes/src/evaluation/online_evaluation.py"

current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)
kafka_ratings_file = "/home/cdgamaro/group-project-s23-the-incredi-codes/data/data_monitor/kafka_ratings_%s.csv" % time_stamp
kafka_recommend_file = "/home/cdgamaro/group-project-s23-the-incredi-codes/data/data_monitor/kafka_recommend_%s.csv" % time_stamp

# model path according to the current running model
current_model = "/home/cdgamaro/group-project-s23-the-incredi-codes/src/models/model_current.pkl" 

print("Rating logs file: ", kafka_ratings_file)
print("Recommend logs file: ", kafka_recommend_file)
print("Model file: ", current_model)

result = subprocess.run(["/usr/bin/python3", rating_reading_file, "hours", "4", kafka_ratings_file], capture_output=True)
# if not "done reading" in result.stdout.decode():
#     print("Could not read data from kafka; exiting")
#     print(result)
#     sys.exit()
print("Ratings logs written to: ", kafka_ratings_file)

result = subprocess.run(["/usr/bin/python3", recommend_reading_file, "hours", "4", kafka_recommend_file], capture_output=True)
# if not "done reading" in result.stdout.decode():
#     print("Could not read data from kafka; exiting")
#     print(result)
#     sys.exit()
print("Recommend logs written to: ", kafka_recommend_file)

result = subprocess.run(["/usr/bin/python3", monitor_file, current_model, kafka_ratings_file, kafka_recommend_file], capture_output=True)
# if not "Model Saved" in result.stdout.decode():
#     print("Model not trained successfully; exiting")
#     print(result)
#     sys.exit()
# print("Model saved to: ", model_pickle_file)

# result = subprocess.run(["sh", "/home/cdgamaro/group-project-s23-the-incredi-codes/deploy.sh", str(time_stamp)], capture_output=True)
# print(result)