
# Movie Recommendation System ![popcorn-large](https://github.com/arpitsahni04/Recommendation-System-End-to-End/assets/81643693/053c2ff3-71c5-4098-ac87-7a3e5af2b114)


This is a project that focuses on the implementaion and operation of a recommendation service in production, which will entail many factors, including deployment, scaling, reliability, drift and feedback loop.

---
## Key Highlights

1. Deployed real-time Recommendation system (collaborative filtering) for 13k movies, 5 Millon users with <800ms response time.'
2. Built data-pipeline to automatically ingest from Kafka stream, and perform data cleaning & quality checks. Established CI/CD using Jenkins, unit tests, and coverage reports.
3. Setup Real-time Model Monitoring with Grafana and Prometheus to check system health and data drift and initiate model retraining. Performed A/B testing for new features in production. Achieved <0.1% downtime during container switching.
4. Developed provenance tracking system using MLFlow to monitor recommendation pipeline, model, and data versions in production.
---

The current folder structure is as follows:
```

├───data
│   ├───data_archive
│   │   ├───data_v1
│   │   ├───data_v2
│   │   └───train_data
│   ├───data_daily
│   ├───data_experimentation
│   ├───data_monitor
│   ├───stats_daily
│   └───__pycache__
├───M4 analysis
├───src
│   ├───data
│   ├───data_read
│   │   └───scripts_archive
│   ├───drift_evaluation
│   ├───evaluation
│   ├───experimentation
│   ├───fairness
│   ├───models
│   │   ├───KNN
│   │   └───SVD
│   ├───monitering
│   │   └───prometheus
│   └───__pycache__
└───tests
    └───__pycache__

```
- Under our data folder, we have uploaded the data in the form of csv files that has been extracted from the kafka streams, cleaned and preprocessed. There're three notebook files which contain the process for data cleaning and information collection.

- The models folder has two pickled model files (SVD and KNN) that we experimented with. It also contains a .ipnyb notebook that contains the code that was used for EDA as well as model training.

- The root folder contains a main.py file which creates and deploys the flask application. This flask application has the /recommend endpoint which makes 20 personalized movie recommendations given a user ID.
```
docker build -t recommender .
docker run -p 8082:8082 -d recommender
```

The VM will start accepting requests on port 8082.

We can check the logs of our docker container as follows:
```
docker logs <container_id> -f
```
