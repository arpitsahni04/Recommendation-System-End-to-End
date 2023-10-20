import os
import sys
import pandas as pd
import numpy as np
import hashlib 


def get_group(x):
    hash_object = hashlib.sha256(str(x).encode('utf-8'))
    groupid = int(hash_object.hexdigest(), 16) % 2
    return groupid

def main():
    # python3 process_telemetry.py ratings_path watching_path
    ratings_path = sys.argv[1]
    watching_path = sys.argv[2]

    ratings = pd.read_csv(ratings_path)
    ratings["group"] = ratings["userid"].apply(get_group)

    ratings[ratings.group == 0].rating.to_csv("ratings_group1.csv", index=False, header=False)
    ratings[ratings.group == 1].rating.to_csv("ratings_group2.csv", index=False, header=False)


    watching = pd.read_csv(watching_path)
    watching_count = watching.groupby("userid")["time"].agg("count").reset_index()
    watching_count["group"] = watching_count["userid"].apply(get_group)

    watching_count[watching_count.group == 0].time.to_csv("watching_group1.csv", index=False, header=False)
    watching_count[watching_count.group == 1].time.to_csv("watching_group2.csv", index=False, header=False)


if __name__=="__main__":
    main()
