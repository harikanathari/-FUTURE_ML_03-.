import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("daily_water_consumption.csv")

# Display first 5 rows
print(df.head())

# Features and Target
X = df[['Age', 'Temperature_C', 'Activity_Level']]
y = df['Water_Consumed_Liters']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction on test data
y_pred = model.predict(X_test)

# Evaluation
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# Example prediction
prediction = model.predict([[25, 30, 2]])
print("Predicted Water Consumption:", prediction[0], "Liters")

# Histogram Output Graph
plt.figure(figsize=(8,5))
plt.hist(df['Water_Consumed_Liters'], bins=10)
plt.title("Water Consumption Distribution")
plt.xlabel("Water Consumed (Liters)")
plt.ylabel("Frequency")
plt.show()
