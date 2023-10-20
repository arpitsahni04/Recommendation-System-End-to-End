import os
import heapq

from compress_pickle import load
from flask import Flask
import pandas as pd
import hashlib

app = Flask(__name__)

path1 = "SVD1.pkl"
path2 = "SVD2.pkl"
model_file1 = os.path.join(os.getcwd(), path1)
model_file2 = os.path.join(os.getcwd(), path2)

pickled_model1 = load(open(model_file1, "rb"), compression="lzma", set_default_extension=False)
pickled_model2 = load(open(model_file2, "rb"), compression="lzma", set_default_extension=False)

movie_df = pd.read_csv("data/movie_list.csv")
df = movie_df[:2500]


def get_predictions(x, model, user_id):
    return model.predict(user_id, x["movieid"]).est


def get_top_recommendations(movieids, ratings, top_N):
    iters = zip(ratings, movieids)
    items = heapq.nlargest(top_N, iters, key = lambda x: x[0])
    return ",".join([x[1] for x in items])


@app.route("/recommend/<int:user_id>")
def recommend_movies(user_id):
    # route the user to two models based on the user_id
    # hash(user_id) % 2 
    hash_object = hashlib.sha256(str(user_id).encode('utf-8'))
    id = int(hash_object.hexdigest(), 16) % 2
    if id == 0:
        ratings = df.apply(get_predictions, args=(pickled_model1, user_id), axis=1)
        top_recommended_movies = get_top_recommendations(df.movieid, ratings, 20)
    else:
        ratings = df.apply(get_predictions, args=(pickled_model2, user_id), axis=1)
        top_recommended_movies = get_top_recommendations(df.movieid, ratings, 20)
    
    return top_recommended_movies


if __name__ == "__main__":  # pragma: no cover
    app.run(port="8082", threaded=True, host=("0.0.0.0"))