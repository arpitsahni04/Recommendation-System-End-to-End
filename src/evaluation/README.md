## Folder Structure

- online_evaluation.py: 
    - calculate the RMSE of the model on new telemetry data
    - parameters are as follows:

```
> python3 online_evaluation.py <model_path> <data_path>

# example
> python3 online_evaluation.py 'algo_SVD_20230322.pkl' 'kafka_ratings_20230323.csv'

```



