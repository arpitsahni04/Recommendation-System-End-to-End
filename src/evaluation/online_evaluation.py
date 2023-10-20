import pandas as pd
import numpy as np
import os
import sys
from compress_pickle import load, dump
from surprise import SVD, accuracy

def get_predictions(x, model):
    return model.predict(x["userid"], x["movieid"]).est

def RMSE(df):
    y_pred = df.rating_est.values
    y_true = df.rating.values
    return (((y_pred - y_true)**2).sum() / y_pred.shape[0]) ** 0.5

def main():
    # python3 online_evaluation.py '../models/SVD/algo_SVD_20230322.pkl' '../../data/data_daily/kafka_ratings_20230323.csv'
    model_path = sys.argv[1]
    data_path = sys.argv[2]

    ratings = pd.read_csv(data_path)
    pickled_model = load(open(model_path, 'rb'), compression="lzma", set_default_extension=False)

    ratings["rating_est"] = ratings.apply(get_predictions, args=(pickled_model,), axis=1)
    print("RMSE on the new telemetry data: %.4f" %RMSE(ratings))


if __name__=='__main__':
    main()
    
