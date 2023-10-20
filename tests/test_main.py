from unittest.mock import patch, mock_open, MagicMock

import pytest
import pandas as pd

from src import main
from src.main import app

test_data = {"movieid": ["nukes+in+space+1999", "mulan+1998", "my+neighbor+totoro+1988", "the+collector+1965", "the+terminator+1984"]} 

def stub_get_predictions():
    return [1,2,3,4]


@patch.object(main, "get_top_recommendations")
@patch.object(main, "get_predictions", return_value=stub_get_predictions(), autospec=True)
@patch.object(main.pd, "read_csv")
@patch.object(main, "load")
def test_index_route(mock_load,
                     mock_read_csv,
                     mock_get_predictions,
                     mock_get_top_recommendations):
    with patch("builtins.open", mock_open(read_data="data")) as mock_file:
        assert open("path/to/open").read() == "data"
    test_df = pd.DataFrame.from_dict(test_data)
    mock_read_csv.return_value = test_df
    mock_get_top_recommendations.return_value = "1,2,3,4"
    response = app.test_client().get("/recommend/1")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "1,2,3,4"


@patch.object(main.pd, "read_csv")
@patch.object(main, "load")
def test_get_predictions(mock_load,
                         mock_read_csv):
    with patch("builtins.open", mock_open(read_data="data")) as mock_file:
        assert open("path/to/open").read() == "data"
    test_model = MagicMock()
    mock_load.return_value = test_model
    test_model.predict.return_value = MagicMock(est=1)
    test_df = pd.DataFrame.from_dict(test_data)
    mock_read_csv.return_value = test_df
    assert main.get_predictions({"movieid": "nukes+in+space+1999"}, test_model, 1) == 1


@patch.object(main.heapq, "nlargest")
@patch.object(main.pd, "read_csv")
@patch.object(main, "load")
def test_get_top_recommendations(mock_load,
                                 mock_read_csv,
                                 mock_nlargest):
    with patch("builtins.open", mock_open(read_data="data")) as mock_file:
        assert open("path/to/open").read() == "data"
    test_df = pd.DataFrame.from_dict(test_data)
    mock_read_csv.return_value = test_df
    mock_nlargest.return_value = [(1, "1"), (2, "2"), (3, "3"), (4, "4")]
    assert main.get_top_recommendations([1,2,3,4], [1,2,3,4], 4) == "1,2,3,4"
