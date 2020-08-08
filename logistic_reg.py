# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 23:12:11 2020

@author: Siddhesh
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Reading dataframe and dropping rows with na values
data = pd.read_csv(r"C:\Users\Dell\PycharmProjects\blogfree\framingham.csv")
data.dropna(inplace=True)  # Consists 3658 records

# Computing Correlation
corr_matrix = data.corr().abs()
high_corr_var = np.where(corr_matrix > 0.35)
high_corr_var = [(corr_matrix.index[x], corr_matrix.columns[y]) for x, y
                 in zip(*high_corr_var) if x != y and x < y]

"""
Variables to consider

age: Age of a person (Input a number)
smoker: Yes or No
Cigs per day: (Input a number)
diabaties: Yes or No
bmi: weight(Kg) and height(meters) calculate
BP: input a number

"""


def bmi(weight, height):
    return round(float(weight) / (float(height) * float(height)), 2)


X_cols = ['male', 'age', 'currentSmoker', 'cigsPerDay', 'diabetes',
          'sysBP', 'BMI']
Y_col = ['TenYearCHD']

X_vars = data[X_cols]
Y_var = data[Y_col]

# Renaming Columns
X_vars.columns = ['Gender', 'Age', 'Smoker', 'Cigarettes_Per_Day',
                  'Diabetic', 'BP', 'BMI']
Y_var.columns = ['Chances_of_hear_disease']

# Splitting data
X_train, X_test, y_train, y_test = train_test_split(X_vars, Y_var,
                                                    test_size=0.25,
                                                    random_state=0)

# Initiate the Model
logreg = LogisticRegression()

# fit the model with data
logreg.fit(X_train, y_train)

pickle.dump(logreg, open('model.pkl', 'wb'))

filename = r'C:\Users\Dell\PycharmProjects\blogfree\model.pkl'
with open(filename, 'rb') as f:
    model = pickle.load(f)

print(model.predict([[1, 30, 0, 0, 0, 80, bmi(70, 1.8)]]))
