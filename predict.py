from flask import Flask
import pickle
from flask import request, jsonify

app= Flask('predict')

with open('model_n=40.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


app = Flask('stroke')

person = {"gender": "Male", "age": 60, "hypertension": 1, "heart_disease":0, "ever_married": "Yes",
          "work_type": "Private", "Residence_type": "Urban", "avg_glucose_level": 150, "bmi": 35,
          "smoking_status" : "formerly smoked"}


@app.route('/predict', methods=['POST'])
def predict():
    person = request.get_json()
    X = dv.transform([person])
    y_pred = model.predict_proba(X)[:, 1]

    result = {
        'probability': float(y_pred)
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)




