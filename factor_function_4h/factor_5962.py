import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, divide, ts_std_dev, log, ts_mean

def factor_5962(data, **kwargs):
    """
    因子名称: Volatility_Momentum_Divergence_38103
    数学表达式: ts_decay_linear(divide(ts_std_dev(log(close), 20), ts_std_dev(log(vol), 20)), d=10) - ts_decay_linear(divide(ts_mean(log(close), 20), ts_mean(log(vol), 20)), d=10)
    中文描述: 该因子计算收盘价对数收益率与成交量对数变化在长期窗口（20天）内的波动性比率的短期线性衰减平均值，与收盘价对数收益率与成交量对数变化在长期窗口（20天）内的均值比率的短期线性衰减平均值之差。通过对数变换平滑价格和成交量的绝对变化，并使用线性衰减加权平均突出近期比率的影响。创新点在于同时考虑了价格/成交量比率的波动性和均值，并使用线性衰减加权，捕捉波动性比率和均值比率的近期趋势差异。如果波动性比率的衰减平均值高于均值比率的衰减平均值，可能预示着近期价格相对于成交量的波动性正在增强，反之则可能预示着均值水平的变化更为显著。该因子可用于识别市场驱动力的变化和潜在的趋势反转信号。
    因子应用场景：
    1. 识别市场驱动力的变化：当波动性比率的衰减平均值高于均值比率的衰减平均值时，可能预示着近期价格相对于成交量的波动性正在增强，反之则可能预示着均值水平的变化更为显著。
    2. 潜在的趋势反转信号：该因子可用于识别潜在的趋势反转信号。
    """
    # 1. 计算 log(close)
    log_close = log(data['close'])
    # 2. 计算 log(vol)
    log_vol = log(data['vol'])
    # 3. 计算 ts_std_dev(log(close), 20)
    ts_std_dev_log_close = ts_std_dev(log_close, d=20)
    # 4. 计算 ts_std_dev(log(vol), 20)
    ts_std_dev_log_vol = ts_std_dev(log_vol, d=20)
    # 5. 计算 divide(ts_std_dev(log(close), 20), ts_std_dev(log(vol), 20))
    divide_std = divide(ts_std_dev_log_close, ts_std_dev_log_vol)
    # 6. 计算 ts_decay_linear(divide(ts_std_dev(log(close), 20), ts_std_dev(log(vol), 20)), d=10)
    ts_decay_linear_std = ts_decay_linear(divide_std, d=10)
    # 7. 计算 ts_mean(log(close), 20)
    ts_mean_log_close = ts_mean(log_close, d=20)
    # 8. 计算 ts_mean(log(vol), 20)
    ts_mean_log_vol = ts_mean(log_vol, d=20)
    # 9. 计算 divide(ts_mean(log(close), 20), ts_mean(log(vol), 20))
    divide_mean = divide(ts_mean_log_close, ts_mean_log_vol)
    # 10. 计算 ts_decay_linear(divide(ts_mean(log(close), 20), ts_mean(log(vol), 20)), d=10)
    ts_decay_linear_mean = ts_decay_linear(divide_mean, d=10)
    # 11. 计算 ts_decay_linear(divide(ts_std_dev(log(close), 20), ts_std_dev(log(vol), 20)), d=10) - ts_decay_linear(divide(ts_mean(log(close), 20), ts_mean(log(vol), 20)), d=10)
    factor = ts_decay_linear_std - ts_decay_linear_mean

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()