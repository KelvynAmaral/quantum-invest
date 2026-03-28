import numpy as np
import pandas as pd

def calculate_metrics(df_f, pesos, rf_daily):
    w_series = pd.Series(pesos) / 100
    df_f['Portfolio'] = df_f[list(pesos.keys())].mul(w_series).sum(axis=1)
    df_calc = df_f.dropna(subset=['Portfolio', 'BRAX11']).copy()
    
    acum_port = (1 + df_calc['Portfolio']).cumprod()
    acum_idx = (1 + df_calc['BRAX11']).cumprod()
    
    vol = df_calc['Portfolio'].std() * (252**0.5)
    sharpe = ((df_calc['Portfolio'] - rf_daily).mean() * 252) / vol if vol > 0 else 0
    beta = df_calc['Portfolio'].cov(df_calc['BRAX11']) / df_calc['BRAX11'].var()
    alpha = ((df_calc['Portfolio'] - rf_daily).mean() - beta * (df_calc['BRAX11'] - rf_daily).mean()) * 252
    
    return {
        "df_calc": df_calc,
        "acum_port": acum_port,
        "acum_idx": acum_idx,
        "sharpe": sharpe,
        "beta": beta,
        "alpha": alpha,
        "vol": vol,
        "max_dd": (acum_port / acum_port.cummax() - 1).min(),
        "var_95": np.percentile(df_calc['Portfolio'], 5)
    }