
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, recall_score
import pickle

df = pd.read_csv('healthcare-dataset-stroke-data.csv')
df.head()

# model params
max_depth = 2
n_estimators = 40
output_file = f'model_n={n_estimators}.bin'

# data preparation
df.columns = df.columns.str.lower()
df.bmi.fillna(df.bmi.mean(), inplace=True)

categorical = ['gender', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'residence_type', 'smoking_status']
numerical = ['age','avg_glucose_level', 'bmi']

df.drop(3116, axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)

df.drop('id', axis=1, inplace=True)

#df.gender = df.gender.map({'Male' :1, 'Female' : 0})
#df.ever_married = df.ever_married.map({'Yes' :1, 'No' : 0})
#df.residence_type = df.residence_type.map({'Urban':1, 'Rural':0})

# train test split
df_train, df_test = train_test_split(df, test_size=0.2, random_state=4)



# One-hot encoding



# Random forest classifier
def train (df_train, n_estimators, max_depth=4):
    y_train = df_train['stroke']
    X_train = df_train.drop('stroke', axis=1)

    dv = DictVectorizer(sparse=True)
    train_dict = X_train.to_dict(orient='records')
    X_train = dv.fit_transform(train_dict)
    model = RandomForestClassifier(random_state=4, max_depth=max_depth, n_estimators=n_estimators,
                                   class_weight='balanced')
    model.fit(X_train, y_train)

    return dv, model


def predict(df, dv, model):
    X = df.drop('stroke', axis=1)

    test_dict = X.to_dict(orient='records')
    X = dv.transform(test_dict)
    y_pred = model.predict_proba(X)[:, 1]
    #y_pred = model.predict(X)

    return y_pred



# training the final model

dv, model = train(df_train, n_estimators, max_depth)
y_pred = predict(df_test, dv, model)

y_test = df_test['stroke']

print("ROC AUC:", roc_auc_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred.round()))

with open(output_file, 'wb') as f_out:
    pickle.dump((dv, model), f_out)

