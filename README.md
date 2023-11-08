# Stroke prediction
## Table of contents
- [Problem description](https://github.com/boiarchuk-m/Stroke-prediction/tree/main#problem-description)
- [About the dataset](https://github.com/boiarchuk-m/Stroke-prediction/tree/main#about-the-dataset)
- [Repository files](https://github.com/boiarchuk-m/Stroke-prediction/tree/main#repository-files)
- [How to install dependencies](https://github.com/boiarchuk-m/Stroke-prediction/tree/main#how-to-install-dependencies)
- [Host the server](https://github.com/boiarchuk-m/Stroke-prediction/tree/main#host-the-server)
- [Making a prediction](https://github.com/boiarchuk-m/Stroke-prediction/tree/main#making-a-prediction)
- [Docker containerization](https://github.com/boiarchuk-m/Stroke-prediction/tree/main#docker-containerization)
- [Cloud deployment](https://github.com/boiarchuk-m/Stroke-prediction/tree/main#cloud-deployment)

## Problem description
According to the World Health Organization (WHO), stroke is the second leading cause of death worldwide, accounting for about 11% of all deaths.Early diagnosis and treatment of stroke is essential to reduce  mortality and related morbidity.

This  project is aimed to create a model that predicts whether a patient is likely to get a stroke based on the input parameters like gender, age, various diseases, and smoking status.

## About the dataset
This dataset was taken from kaggle : https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset. Dataset contains 5110 observations with 12 attributes.  

Attribute Information:
 1. id: unique identifier
 2. gender: "Male", "Female" or "Other"
 3. age: age of the patient
 4. hypertension: 0 if the patient doesn't have hypertension, 1 if the patient has hypertension
 5. heart_disease: 0 if the patient doesn't have any heart diseases, 1 if the patient has a heart disease
 6. ever_married: "No" or "Yes"
 7. work_type: "children", "Govt_jov", "Never_worked", "Private" or "Self-employed"
 8. Residence_type: "Rural" or "Urban"
 9. avg_glucose_level: average glucose level in blood
 10. bmi: body mass index
 11. smoking_status: "formerly smoked", "never smoked", "smokes" or "Unknown"*
 12. stroke: 1 if the patient had a stroke or 0 if not

## Repository files
- `notebook.ipynb` jupyter notebook with EDA and models development
- `train.py` a python script to train a model
- `model_n=40.bin` binary file with trained model and dictvectorizer
- `healthcare-dataset-stroke-data.csv` dataset
- `Pipfile` and `Pipfile.lock` files with dependencies for environment
- `predict.py` a python script to create a web service based on the model
- `request.py` a python script to send a request to the service and check it's work
- `Dockerfile` a script to generate docker container
- `request_cloud.py` a python script to send a request to the cloud service

## How to install dependencies
If you don't have `pipenv`, install it using this command
```bash
  pip install pipenv
```
Install needed packages to the virtual environment
```bash
  pipenv install
```
Activate virtual environment
```bash
  pipenv shell
```

## Host the server
You can host the server using this command
```bash
  python predict.py
```
Or using waitress 
```bash
  waitress-serve --listen=0.0.0.0:9696 predict:app
```
## Making a prediction

To check the work of the web server you can use file `request.py` 
Just run it with this command
```bash
   python request.py
```
This file contains a dictionary `person`. You can try to change some features and see how prediction will change.
```python
  person = {"gender": "Male", "age": 60, "hypertension": 1, "heart_disease":0, "ever_married": "Yes",
          "work_type": "Private", "Residence_type": "Urban", "avg_glucose_level": 150, "bmi": 35,
          "smoking_status" : "formerly smoked"}
```
In the output you will get the probability of the stroke
```bash
   {'probability': 0.6324732591245272}

```
## Docker containerization

You can run a web server using docker. First you need to create a docker image using the Dockerfile. Go to the project folder and run this command
```bash
   docker build -t stroke-prediction .
```
Now, just use the command below and the model will be served to your local host, and you can make a prediction in the same way as explained above
```bash
   docker run -it -p 9696:9696 stroke-prediction:latest
```

## Cloud deployment

The web service was deployed to the google cloud and here are steps how I made it.

First you need to install the gcloud CLI.There is an instructions form google how to make it: https://cloud.google.com/sdk/docs/install

Then you need to open the Google Cloud CLI shell and log in your account 
```bash
    gcloud auth login
```
After this you need to configure Docker 
```bash
    gcloud auth configure-docker
```
Then, create a project
```bash
    gcloud config set project midterm-project-404508
```
Tag an image 
```bash
docker tag mid_project gcr.io/midterm-project-404508/mid_project
```
Push image to Google Container Registry
```bash
docker push gcr.io/midterm-project-404508/mid_project
```
Deploy image
```bash
gcloud run deploy mid-project gcr.io/midterm-project-404508/mid_project --port 9696 --platform managed --region us-central1
```

Here is a url to test this cloud service: https://mid-project-2gonzmac4a-uc.a.run.app/predict
Also, you can use the file `request_cloud.py` that uses this link to make a request.
