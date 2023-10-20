## Folder Structure

- experiment.py: 
    - Defines a class MovieRecommendationExperiment that does the following:
        - loads rating sets and watching log sets for two models for comparison
        - performs A/B testing and evaluates metric performance of model A and model B for both rating set and watching logs
    - parameters are as follows:
        - rating set A path: the path for the first model's ratings
        - rating set B path: the path for the second model's ratings
        - watching log A path: the path for the first model's watch time logs
        - watching log B path: the path for the second model's watch time logs


```
# how to run the file:
> python src/experimentation/experiment.py <rating set A path> <rating set B path> <watching log A path> <watching log B path>

# example
> python src/experimentation/experiment.py data/data_experimentation/ratings_group1.csv data/data_experimentation/ratings_group2.csv data/data_experimentation/watching_group1.csv data/data_experimentation/watching_group2.csv

```



