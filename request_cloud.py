import requests

host = 'https://mid-project-2gonzmac4a-uc.a.run.app'
url = f'{host}/predict'

person = {"gender": "Male", "age": 60, "hypertension": 1, "heart_disease":0, "ever_married": "Yes",
          "work_type": "Private", "Residence_type": "Urban", "avg_glucose_level": 150, "bmi": 35,
          "smoking_status" : "formerly smoked"}

response = requests.post(url, json=person).json()
print(response)