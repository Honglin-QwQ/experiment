import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_covariance, ts_decay_exp_window, ts_delta, multiply

def factor_5973(data, **kwargs):
    """
    因子名称: Vol_Price_Cov_Decay_54702
    数学表达式: multiply(ts_covariance(volume, vwap, 90), ts_decay_exp_window(ts_delta(vwap, 30), 60, 0.7))
    中文描述: 该因子结合了交易量与成交量加权平均价格（VWAP）的协方差以及VWAP的指数衰减动量。首先，它计算过去90天内交易量和VWAP的协方差，衡量两者之间的同步性。然后，计算过去30天VWAP的变化量，并对这个变化量应用一个窗口期为60天、衰减因子为0.7的指数衰减加权平均。最后，将两者相乘。这个因子旨在捕捉交易量和价格之间的长期关系，并结合近期价格动量的指数衰减影响。协方差部分可以识别价量齐升或背离的情况，而指数衰减动量部分则对近期价格趋势给予更大的权重。这可能用于识别在特定价量关系背景下具有持续或反转动量的股票。相较于参考因子，创新点在于结合了长期协方差和指数衰减的短期动量，并使用了ts_decay_exp_window运算符。
    因子应用场景：
    1. 识别交易量和价格之间的长期关系。
    2. 捕捉近期价格动量的指数衰减影响。
    3. 识别在特定价量关系背景下具有持续或反转动量的股票。
    """
    # 1. 计算 ts_covariance(volume, vwap, 90)
    data_ts_covariance = ts_covariance(data['vol'], data['vwap'], 90)
    # 2. 计算 ts_delta(vwap, 30)
    data_ts_delta_vwap = ts_delta(data['vwap'], 30)
    # 3. 计算 ts_decay_exp_window(ts_delta(vwap, 30), 60, 0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_delta_vwap, 60, 0.7)
    # 4. 计算 multiply(ts_covariance(volume, vwap, 90), ts_decay_exp_window(ts_delta(vwap, 30), 60, 0.7))
    factor = multiply(data_ts_covariance, data_ts_decay_exp_window)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()