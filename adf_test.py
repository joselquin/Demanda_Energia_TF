# Función para Augmented Dickey-Fuller test
# Este test detecta si la serie temporal es o no estacionaria
# (c) Pierian Data  - www.pieriandata.com

from statsmodels.tsa.stattools import adfuller
import pandas as pd

def adf_test(series):
    
    print(f'Augmented Dickey-Fuller Test')
    result = adfuller(series.dropna(),autolag='AIC')
    
    labels = ['ADF test','p-value','# lags','# observaciones']
    out = pd.Series(result[0:4],index=labels)

    for key,val in result[4].items():
        out[f'critical value ({key})']=val
        
    print(out.to_string())
    
    if result[1] <= 0.05:
        print("Rechazamos la hipótesis nula")
        print("La serie es estacionaria")
    else:
        print("No se puede rechazar la hipótesis nula")
        print("La serie es no estacionaria")