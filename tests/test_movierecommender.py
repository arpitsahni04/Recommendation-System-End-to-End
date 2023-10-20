from unittest.mock import patch, mock_open, MagicMock
import pytest
import pandas as pd
from surprise import SVD, Reader
from surprise.dataset import DatasetAutoFolds
import os
import io
from contextlib import redirect_stdout
from src.models import movierecommender


def test_data_prepare():
    ratings = pd.DataFrame({"userid":[1,1,2,3,3], 
                            "movieid":["m1","m2","m1","m2","m3"],
                            "rating":[3,4,4,5,5]})
    res = movierecommender.data_prepare(ratings)
    assert len(res[1]) == 1
    
    
def test_model_fit():
    algo = SVD()
    reader = Reader(rating_scale = (1,5))
    ratings = pd.DataFrame({"userid":[1,1,2,2], 
                            "movieid":["m1","m2","m1","m2"],
                            "rating":[2,4,4,2]})
    training_df = DatasetAutoFolds(df=ratings, reader=reader).build_full_trainset()
    movierecommender.model_fit(algo, training_df)
    assert algo.predict(1,"m1").est <= 5 and algo.predict(1,"m1").est >= 1
    
    
def test_offline_evaluation():
    algo = SVD()
    reader = Reader(rating_scale = (1,5))
    ratings = pd.DataFrame({"userid":[1,1,2,2], 
                            "movieid":["m1","m2","m1","m2"],
                            "rating":[2,4,4,2]})
    df = DatasetAutoFolds(df=ratings, reader=reader).build_full_trainset()
    algo.fit(df)
    rmse = movierecommender.offline_evaluation(algo, df.build_testset()) 
    assert rmse < 2 and rmse > 0


def test_save_model():
    algo = SVD()
    save_path = "tmp.pkl"
    movierecommender.save_model(algo, save_path)
    assert os.path.exists(save_path)
    
    
def test_measure_size():
    save_path = "tmp.pkl"
    assert movierecommender.measure_size(save_path) > 1e-5
    os.remove(save_path)
    

def test_get_predictions():
    test_model = MagicMock()
    test_model.predict.return_value = MagicMock(est=1)
    assert movierecommender.get_predictions({"movieid": "m1"}, test_model, 1) == 1


def test_get_top_recommendations():
    movieids = ["a","b","c","d"]
    ratings = [1,2,3,4]
    assert movierecommender.get_top_recommendations(movieids, ratings, 2) == "d,c"


def test_recommend_movies():
    test_model = MagicMock()
    test_model.predict.return_value = MagicMock(est=1)
    movie_df = pd.DataFrame({"movieid": ["m1","m2"]})
    assert movierecommender.recommend_movies(test_model, 1, movie_df) == "m1,m2"
    
    
def test_measure_inference_time():
    ratings = pd.DataFrame({"userid":[1,2,3,4,5,6,7,8,9,10]})
    movie_df = pd.DataFrame({"movieid": ["m1","m2"]})
    svd = MagicMock(return_value=1)
    t = movierecommender.measure_inference_time(ratings, svd, movie_df)
    assert type(t) == float and t > 0


@patch.object(movierecommender, "measure_inference_time")
@patch.object(movierecommender, "measure_size")
@patch.object(movierecommender, "save_model")
@patch.object(movierecommender, "offline_evaluation")
@patch.object(movierecommender, "model_fit")
@patch.object(movierecommender, "data_prepare")
@patch.object(movierecommender.pd, "read_csv")
def test_main(mock_read_csv, 
              mock_data_prepare, 
              mock_model_fit, 
              mock_offline_evaluation, 
              mock_save_model,
              mock_measure_size,
              mock_measure_inference_time):
    ratings = pd.DataFrame({"userid":[1,1,2,3,3], 
                            "movieid":["m1","m2","m1","m2","m3"],
                            "rating":[3,4,4,5,5]})
    mock_read_csv.return_value = ratings
    mock_data_prepare.return_value = ratings, ratings
    mock_model_fit.return_value = 0.1
    mock_offline_evaluation.return_value = 0.5
    mock_measure_size.return_value = 0.1
    mock_measure_inference_time.return_value = 1
    
    f = io.StringIO()
    with redirect_stdout(f):
        movierecommender.main()
    res = f.getvalue()

    ref = "Data Loaded\nmodel init\nmodel Trained\nModel Training Time : 0.1\nModel test set RMSE (offline): 0.5000\nModel Size : 0.1\nAverage_inference_time 1\n"
    assert ref == res
