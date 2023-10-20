from unittest.mock import patch, mock_open, MagicMock
import pytest
import pandas as pd
import io
from contextlib import redirect_stdout
from src.evaluation import online_evaluation


def test_online_RMSE():
    df = pd.DataFrame({"rating":[1,2,3,4], "rating_est":[2,2,3,4]})
    assert online_evaluation.RMSE(df) == 0.5

    
@patch.object(online_evaluation, "load")
def test_online_get_predictions(mock_load):
    test_model = MagicMock()
    mock_load.return_value = test_model
    test_model.predict.return_value = MagicMock(est=1)
    assert online_evaluation.get_predictions({"userid": 11, "movieid":"nukes+in+space+1999", "rating":3}, test_model) == 1
    
    
@patch.object(online_evaluation, "RMSE")
@patch.object(online_evaluation, "load")
@patch.object(online_evaluation.pd, "read_csv")
@patch.object(online_evaluation.sys, "argv")
def test_main(mock_argv, mock_read_csv, mock_load, mock_RMSE):
    mock_argv[1] = 1
    mock_argv[2] = 2
    mock_read_csv.return_value = pd.DataFrame({"userid":[1,1,2,3,3], 
                            "movieid":["m1","m2","m1","m2","m3"],
                            "rating":[3,4,4,5,5]})
    test_model = MagicMock()
    test_model.predict.return_value = MagicMock(est=1)
    mock_load.return_value = test_model
    mock_RMSE.return_value = 0.5
        
    f = io.StringIO()
    with redirect_stdout(f):
        online_evaluation.main()
    res = f.getvalue()
    
    ref = "RMSE on the new telemetry data: 0.5000\n"
    assert res == ref