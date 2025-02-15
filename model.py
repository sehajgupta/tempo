import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

df_train = pd.read_csv("job-salary-prediction/Train_rev1.zip", 
                 compression='zip',  header=0, sep=',', quotechar='"')

for label, content in df_train.items():
    if pd.api.types.is_string_dtype(content):
        df_train[label] = content.astype("category").cat.as_ordered()

for label,content in df_train.items():
    if not pd.api.types.is_numeric_dtype(content):
        # Add binary column to indicate whether sample had missing value
        df_train[label+"is_missing"]=pd.isnull(content)
        # Turn categories into numbers and add+1
        df_train[label] = pd.Categorical(content).codes+1

df_copy = df_train.copy()

X = df_copy.drop(columns=["SalaryNormalized"],axis=1)
y = df_copy["SalaryNormalized"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)
model = RandomForestRegressor(n_jobs=-1)

model.fit(X_train,y_train)

joblib.dump(model, "model.pk1")
