
# A Movie Recommendation System

This is a project that focuses on the implementaion and operation of a recommendation service in production, which will entail many factors, including deployment, scaling, reliability, drift and feedback loop.

The current folder structure is as follows:

- Under our data folder, we have uploaded the data in the form of csv files that has been extracted from the kafka streams, cleaned and preprocessed. There're three notebook files which contain the process for data cleaning and information collection.

- The models folder has two pickled model files (SVD and KNN) that we experimented with. It also contains a .ipnyb notebook that contains the code that was used for EDA as well as model training.

- The root folder contains a main.py file which creates and deploys the flask application. This flask application has the /recommend endpoint which makes 20 personalized movie recommendations given a user ID.

We have deployed our flask app to our VM as an isolated docker container, the Dockerfile for this is also in the root folder.

In order to redeploy the service on the VM, ssh into the VM and navigate to the root folder of the project. Then, run the following commands:

```
docker build -t recommender .
docker run -p 8082:8082 -d recommender
```

The VM will start accepting requests on port 8082.

We can check the logs of our docker container as follows:
```
docker logs <container_id> -f
```
