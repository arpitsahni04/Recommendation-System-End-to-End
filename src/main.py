import os
import heapq

from compress_pickle import load
from flask import Flask
import pandas as pd

timestamp = os.getenv("timestamp")
if not timestamp:
    model_file = os.path.join(os.getcwd(), "models/SVD/algo_SVD.pkl")
else:
    model_file = os.path.join(os.getcwd(), f"models/model_{timestamp}.pkl")

app = Flask(__name__)

pickled_model = load(open(model_file, "rb"), compression="lzma", set_default_extension=False)
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
    ratings = df.apply(get_predictions, args=(pickled_model, user_id), axis=1)
    top_recommended_movies = get_top_recommendations(df.movieid, ratings, 20)
    return top_recommended_movies


if __name__ == "__main__":  # pragma: no cover
    app.run(port="8082", threaded=True, host=("0.0.0.0"))
