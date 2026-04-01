import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Load dataset (FIXED)
cols = ['unit','cycle'] + [f'op{i}' for i in range(1,4)] + [f's{i}' for i in range(1,22)]
train = pd.read_csv('train_FD001.txt', delim_whitespace=True, header=None)
train = train.iloc[:, :26]
train.columns = cols

# RUL calculation (FIXED)
max_cycle = train.groupby('unit')['cycle'].max().reset_index()
max_cycle.rename(columns={'cycle': 'max_cycle'}, inplace=True)

# Merge back
train = train.merge(max_cycle, on='unit', how='left')

# Compute RUL
train['RUL'] = train['max_cycle'] - train['cycle']

# Drop extra column
train.drop('max_cycle', axis=1, inplace=True)

# Normalize (FIXED typo)
scaler = MinMaxScaler()
features = train.columns.difference(['unit','cycle','RUL'])
train[features] = scaler.fit_transform(train[features])

# Create sequences (FIXED indentation)
def create_sequences(df, seq_length=30):
    X, y = [], []
    
    for unit in df['unit'].unique():
        unit_df = df[df['unit'] == unit]
        
        for i in range(len(unit_df) - seq_length):
            X.append(unit_df.iloc[i:i+seq_length][features].values)
            y.append(unit_df.iloc[i+seq_length]['RUL'])
    
    return np.array(X), np.array(y)

X, y = create_sequences(train)

print("Data shape:", X.shape, y.shape)

# Model
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# Train
model.fit(X, y, epochs=5, batch_size=64)

# Save
model.save("model/lstm_model.keras")

print("Model trained and saved!")