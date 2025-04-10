# 🚗 Car Price Predictor

A machine learning project that predicts used car prices based on features like brand, mileage, age, and more. Built with a TensorFlow/Keras model and a React + Vite frontend.

---

## 🔧 How It Works

1. **Data Cleaning**: Removes symbols, handles missing values, filters outliers.
2. **Feature Engineering**: Creates new features like car age and mileage per year.
3. **Encoding**: One-hot encodes categorical features and scales numerical ones.
4. **Model**: A neural network trained on log-transformed car prices.
5. **Prediction**: Returns the estimated price using the trained model.

---

## 🧠 Model Tech

- **Framework**: TensorFlow / Keras
- **Preprocessing**: Pandas, NumPy, Scikit-learn
- **Evaluation**: MAE, RMSE, R²
- **Output**: `model.pkl`, `scaler.pkl`, `columns.pkl`

---

## 🖥️ Frontend

- **Framework**: React + Vite
- **Function**: Takes car info input and displays predicted price
