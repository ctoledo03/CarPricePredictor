import pandas as pd
import numpy as np
import re
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

csv_path = os.path.join(os.path.dirname(__file__), 'used_cars.csv')
df = pd.read_csv(csv_path)

df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
df['milage'] = df['milage'].replace(r'[^0-9]', '', regex=True).astype(int)

df['clean_title'] = df['clean_title'].map({'Yes': 1, 'No': 0}).fillna(0)
df['accident'] = df['accident'].apply(lambda x: 0 if 'None reported' in str(x) else 1)

current_year = pd.Timestamp.now().year
df['age'] = current_year - df['model_year']
df['milage_per_year'] = df['milage'] / (df['age'] + 1)

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)
low, high = df['price'].quantile([0.01, 0.99])
df = df[(df['price'] >= low) & (df['price'] <= high)]

df['log_price'] = np.log1p(df['price'])
y = df['log_price']

numeric_features = ['age', 'milage', 'milage_per_year']
categorical_features = ['brand', 'fuel_type', 'transmission', 'ext_col', 'int_col']
binary_features = ['clean_title', 'accident']

def encode_categorical(df, columns, min_freq=0.05):
    for col in columns:
        counts = df[col].value_counts(normalize=True)
        top_categories = counts[counts > min_freq].index
        df[col] = df[col].where(df[col].isin(top_categories), 'Other')
    return pd.get_dummies(df, columns=columns, drop_first=True)

df_encoded = encode_categorical(df[numeric_features + categorical_features + binary_features], categorical_features)

X = df_encoded

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1)
])
model.compile(optimizer=Adam(learning_rate=0.01), loss='mse')

early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(
    X_train_scaled, y_train,
    validation_data=(X_test_scaled, y_test),
    epochs=100,
    batch_size=32,
    callbacks=[early_stop],
    verbose=1
)

y_pred_log = model.predict(X_test_scaled).flatten()
y_pred = np.expm1(y_pred_log)
y_true = np.expm1(y_test)

print(f"MAE: ${mean_absolute_error(y_true, y_pred):.2f}")
print(f"RMSE: ${np.sqrt(mean_squared_error(y_true, y_pred)):.2f}")
print(f"R²: {r2_score(y_true, y_pred):.4f}")

save_dir = os.path.dirname(__file__)
with open(os.path.join(save_dir, 'model.pkl'), 'wb') as f:
    pickle.dump(model, f)
with open(os.path.join(save_dir, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)
with open(os.path.join(save_dir, 'columns.pkl'), 'wb') as f:
    pickle.dump(X.columns.tolist(), f)
