import pickle
import numpy as np
import pandas as pd
import os
import traceback 

model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'scaler.pkl')
columns_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'columns.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)
with open(scaler_path, 'rb') as f:
    scaler = pickle.load(f)
with open(columns_path, 'rb') as f:
    column_order = pickle.load(f)

def map_fuel_type(val):
    if isinstance(val, str):
        return val
    mapping = {
        0: 'Gasoline',
        1: 'Hybrid',
        2: 'Diesel',
        3: 'Electric',
        4: 'E85 Flex Fuel'
    }
    return mapping.get(int(val), 'Other')

def build_input_df(data):
    current_year = pd.Timestamp.now().year
    model_year = int(data['model_year'])
    milage = int(data['milage'])
    age = current_year - model_year
    milage_per_year = milage / (age + 1)

    fuel = map_fuel_type(data['fuel_type'])
    clean_title = int(data['clean_title'])
    accident = int(data.get('accident', 0))
    transmission = data.get('transmission', 'Other')
    brand = data.get('brand', 'Other')
    model = data.get('model', 'Other')
    engine = data.get('engine', '') 
    ext_col = data.get('ext_col', 'Other')
    int_col = data.get('int_col', 'Other')

    base_input = {
        'age': age,
        'milage': milage,
        'milage_per_year': milage_per_year,
        'brand': brand,
        'model': model, 
        'fuel_type': fuel,
        'transmission': transmission,
        'ext_col': ext_col,
        'int_col': int_col,
        'clean_title': clean_title,
        'accident': accident
    }

    df = pd.DataFrame([base_input])
    df_encoded = pd.get_dummies(df, columns=['brand', 'model', 'transmission', 'fuel_type', 'ext_col', 'int_col'], drop_first=False)

    for col in column_order:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    df_encoded = df_encoded[column_order]

    return df_encoded

def predict_price(data):
    try:
        df_input = build_input_df(data)
        X_scaled = scaler.transform(df_input)
        log_pred = model.predict(X_scaled)[0][0]
        price = np.expm1(log_pred)
        return round(price, 2)
    except Exception as e:
        print("Prediction error:", e)
        traceback.print_exc() 
        return None
