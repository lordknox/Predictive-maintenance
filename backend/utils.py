import numpy as np
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

def preprocess_input(data):
    data = np.array(data)
    
    if len(data.shape) == 2:
        data = scaler.fit_transform(data)
        data = np.expand_dims(data,axis=0)
    return data