# -*- coding: utf-8 -*-
"""car Price .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18B21SplyeQe9KosN4t0esICoOfuCeRY_
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler

data_path = '/content/archive (14).zip'
data = pd.read_csv(data_path)

data['Car_Age'] = 2024 - data['Year']
data.drop(['Year', 'Car_Name'], axis=1, inplace=True)

categorical_cols = ['Fuel_Type', 'Selling_type', 'Transmission']
one_hot_encoder = OneHotEncoder()
categorical_encoded = one_hot_encoder.fit_transform(data[categorical_cols]).toarray()
categorical_feature_names = one_hot_encoder.get_feature_names_out(categorical_cols)

numerical_data = data.drop(categorical_cols, axis=1)
data_encoded = pd.DataFrame(
    np.hstack([numerical_data.values, categorical_encoded]),
    columns=list(numerical_data.columns) + list(categorical_feature_names)
)

X = data_encoded.drop('Selling_Price', axis=1)
y = data_encoded['Selling_Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestRegressor(random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("Root Mean Squared Error:", np.sqrt(mean_squared_error(y_test, y_pred)))

sns.histplot(data['Selling_Price'], kde=True, bins=20)
plt.title('Distribution of Selling Price')
plt.xlabel('Selling Price (in Lakhs)')
plt.show()

sns.heatmap(data_encoded.corr(), annot=False, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

print("\nProvide car details for price prediction:")
present_price = float(input("Enter Present Price (in Lakhs): "))
driven_kms = int(input("Enter Kilometers Driven: "))
car_age = int(input("Enter Car Age: "))
fuel_type = input("Enter Fuel Type (Petrol/Diesel/CNG): ")
selling_type = input("Enter Selling Type (Dealer/Individual): ")
transmission = input("Enter Transmission Type (Manual/Automatic): ")
owner = int(input("Enter Number of Previous Owners: "))

input_data = {
    'Present_Price': present_price,
    'Driven_kms': driven_kms,
    'Owner': owner,
    'Car_Age': car_age,
    'Fuel_Type_Diesel': 1 if fuel_type == 'Diesel' else 0,
    'Fuel_Type_Petrol': 1 if fuel_type == 'Petrol' else 0,
    'Fuel_Type_CNG': 1 if fuel_type == 'CNG' else 0,
    'Selling_type_Dealer': 1 if selling_type == 'Dealer' else 0,
    'Selling_type_Individual': 1 if selling_type == 'Individual' else 0,
    'Transmission_Automatic': 1 if transmission == 'Automatic' else 0,
    'Transmission_Manual': 1 if transmission == 'Manual' else 0
}

input_df = pd.DataFrame([input_data], columns=X.columns)

input_scaled = scaler.transform(input_df)

predicted_price = model.predict(input_scaled)[0]

print(f"\nPredicted Selling Price: {predicted_price:.2f} Lakhs")