import time
import sys
import os
import pandas as pd
import surprise
import numpy as np
from compress_pickle import load,dump
import time
from surprise import KNNWithMeans, SVD, accuracy, Dataset, Reader
from surprise.model_selection import train_test_split
import datetime
import heapq
import mlflow
import mlflow.sklearn
from git import Repo

# def init_svd():
#     # similarity = {
#     # "name":"cosine",
#     # "user_based": False #item-based similarity
#     # }
#     # algo_KNN = KNNWithMeans(sim_options=similarity)

#     #SVD
#     algo_SVD = SVD()
#     return algo_SVD


## define train test function
# def train_test_algo(algo,ratings,T):
#     reader = Reader(rating_scale = (1,5))
#     rating_df = Dataset.load_from_df(ratings[['userid', 'movieid', 'rating']], reader)
#     training_set, testing_set = train_test_split(rating_df, test_size = 0.2)
#     start_time = time.time()
#     algo.fit(training_set)
#     end_time = time.time()
#     Training_time = end_time - start_time
#     # print("Training Time :",Training_time)
#     test_output = algo.test(testing_set)
#     test_df = pd.DataFrame(test_output)
#     RMSE = accuracy.rmse(test_output, verbose = False)
#     # MAE = accuracy.mae(test_output, verbose=False)
#     # MSE = accuracy.mse(test_output, verbose=False)
#     # print("RMSE -",label, accuracy.rmse(test_output, verbose = False))
#     # print("MAE -", label, accuracy.mae(test_output, verbose=False))
#     # print("MSE -", label, accuracy.mse(test_output, verbose=False))
#     # dump algo
#     cur = datetime.datetime.now().isoformat()
#     save_path = 'SVD/algo_SVD'+ '_'+T+ '.pkl'
#     dump(algo, save_path, compression="lzma", set_default_extension=False)
#     return algo, test_df, RMSE, Training_time, save_path

def data_prepare(ratings):
    reader = Reader(rating_scale = (1,5))
    rating_df = Dataset.load_from_df(ratings[['userid', 'movieid', 'rating']], reader)
    training_set, testing_set = train_test_split(rating_df, test_size = 0.1)
    return training_set, testing_set

def model_fit(algo, training_set):
    start_time = time.time()
    algo.fit(training_set)
    end_time = time.time()
    Training_time = end_time - start_time
    return Training_time

def offline_evaluation(algo, testing_set):
    test_output = algo.test(testing_set)
    RMSE = accuracy.rmse(test_output, verbose = False)
    return RMSE

def save_model(algo, save_path):
    dump(algo, save_path, compression="lzma", set_default_extension=False)

def measure_size(save_path):
    algo_SVD_size = os.path.getsize(save_path)
    algo_SVD_size /=(1024*1024)
    # print(algo_SVD_size)
    return algo_SVD_size

# return the estimated rating for a (user, movie) pair; used in recommend_movies()
def get_predictions(x, model, user_id):
    return model.predict(user_id, x["movieid"]).est


# calculate the top 20 ratings for a user using heapq; used in recommend_movies()
def get_top_recommendations(movieids, ratings, top_N):
    iters = zip(ratings, movieids)
    items = heapq.nlargest(top_N, iters, key = lambda x: x[0])
    return ",".join([x[1] for x in items])


# return the top 20 movies for a user
def recommend_movies(model, user_id, movie_df):
    ratings_new = movie_df.apply(get_predictions, args=(model, user_id), axis=1)
    top_recommended_movies = get_top_recommendations(movie_df.movieid, ratings_new, 20)
    return top_recommended_movies


def measure_inference_time(ratings, svd, movie_df):
        total_inference_time_svd = 0
        random_user_ids = list(ratings['userid'].sample(n=10, replace=False))            
        for query in random_user_ids:
            start_time = time.time()
            result = recommend_movies(svd, query, movie_df)
            end_time = time.time()
            inference_time_svd = end_time - start_time
            total_inference_time_svd +=inference_time_svd
        average_inference_time_svd = total_inference_time_svd/len(random_user_ids)
        # print("SVD time :",average_inference_time_svd)
        return average_inference_time_svd


def main():
    # python3 movierecommender.py ../data/data_daily/kafka_ratings_xxxx.csv ./model/xxx.pkl

    # get parameters
    data_path = sys.argv[1]
    save_path = sys.argv[2]

    # set up mlflow logging
    # mlflow.set_tracking_uri('http://localhost:5000')
    mlflow.set_experiment('MovieRecommender')

    # start run
    with mlflow.start_run() as run:
    # log parameters
        mlflow.log_param("data_path", data_path)
        mlflow.log_param("save_path", save_path)

        # log git commit id and pipeline version
        repo = Repo(search_parent_directories=True)
        git_commit = repo.head.object.hexsha
        mlflow.set_tag("pipeline version", git_commit)


        # reading rating data
        ratings = pd.read_csv(data_path)
        ratings = ratings.drop_duplicates(subset=["movieid","userid"], keep='last')
        print("Data Loaded")

        # used for prediction
        movie_df = ratings.groupby(["movieid"]).rating.agg(["count"]).reset_index().sort_values(by="count", ascending=False)

        # init svd 
        algo_SVD = SVD(n_factors=100, n_epochs=200)
        print("model init")

        # get test result
        # svd, train_test_SVD, RMSE_svd, Training_Time, save_path = train_test_algo(algo_SVD, ratings, "20230322")
        # Split data into training and testing sets
        training_set, testing_set = data_prepare(ratings)
        Training_Time = model_fit(algo_SVD, training_set)
        rmse = offline_evaluation(algo_SVD, testing_set)

        # save_path = os.path.join("src","models","SVD","algo_SVD.pkl")
        save_model(algo_SVD, save_path)

        print("Model Trained")
        print("Model Training Time :",Training_Time)
        print("Model test set RMSE (offline): %.4f" %rmse)
        print("Model Saved")

        # measure model size
        model_size = measure_size(save_path)
        print("Model Size :",model_size)

        # log metrics and artifacts to mlflow
        mlflow.log_metric("training_time", Training_Time)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("model_size", model_size)

        mlflow.log_artifact(save_path)


        # measure model inference time
        average_inference_time = measure_inference_time(ratings, algo_SVD, movie_df)
        print("Average_inference_time",average_inference_time)

        # log inference time to mlflow
        mlflow.log_metric("average_inference_time", average_inference_time)

        # log model version
        mlflow.sklearn.log_model(algo_SVD, "model", registered_model_name="SVD_model")


    # end run
    mlflow.end_run()   


if __name__=='__main__':

    main()
    
