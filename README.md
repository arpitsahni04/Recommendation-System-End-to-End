
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

# Project Deployment Guide

## Data Files
- Our data is located under the "data" folder in the form of CSV files. These files have been extracted from Kafka streams, cleaned, and preprocessed.

## Notebook Files
- There are three notebook files under the project:
  - Data Cleaning Notebook
  - Information Collection Notebook
  - Other Data Processing Notebook

## Model Files
- The "models" folder contains two pickled model files: SVD and KNN. You can find the code used for model training and Exploratory Data Analysis (EDA) in the "models.ipynb" notebook.

## Flask Application
- The core of our project is the Flask application, which is in the root folder. This application provides a "/recommend" endpoint that offers personalized movie recommendations based on a user's ID.

## Docker Deployment
- We've deployed our Flask app as an isolated Docker container on a virtual machine (VM). The Dockerfile required for this deployment can be found in the root folder.

## Redeployment Instructions
To redeploy the service on your VM, follow these steps:

1. **SSH into the VM**: Access your VM via SSH.

2. **Navigate to Project Root**: After logging into your VM, navigate to the root folder of your project where "main.py" and the Dockerfile are located.

3. **Execute the Following Commands**:

```
docker build -t recommender .
docker run -p 8082:8082 -d recommender
```

The VM will start accepting requests on port 8082.

We can check the logs of our docker container as follows:
```
docker logs <container_id> -f
```
