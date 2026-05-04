import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# 1. Create some sample training data
# Columns: Area, Bedrooms, Bathrooms, Age
data = {
    'area': [1000, 1500, 2000, 2500, 3000, 1200, 1800, 2200],
    'bedrooms': [2, 3, 3, 4, 4, 2, 3, 3],
    'bathrooms': [1, 2, 2, 3, 3, 1, 2, 2],
    'age': [10, 5, 2, 1, 15, 8, 4, 3],
    'price': [35000, 52000, 70000, 88000, 95000, 42000, 63000, 77000]
}

df = pd.DataFrame(data)

# 2. Features and Target
X = df[['area', 'bedrooms', 'bathrooms', 'age']]
y = df['price']

# 3. Train Model
model = LinearRegression()
model.fit(X, y)

# 4. Save Model as pkl
with open('house_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Success: house_model.pkl has been created and saved!")
print(f"Sample prediction for 1500 sqft, 3 bed, 2 bath, 5 years: ₹{model.predict([[1500, 3, 2, 5]])[0]:,.2f}")
