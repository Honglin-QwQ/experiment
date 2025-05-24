import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, multiply, ts_std_dev, adv, divide

def factor_5607(data, **kwargs):
    """
    因子名称: factor_volatility_adjusted_return_45006
    数学表达式: divide(ts_delta(close, 5), multiply(ts_std_dev(close, 20),adv(vol,20)))
    中文描述: 该因子计算过去5天收盘价的变化量，并将其除以过去20天收盘价的标准差与过去20天平均交易量乘积。该因子旨在衡量经波动率调整后的短期价格变动，并结合了成交量信息。创新点在于同时考虑了价格波动率和成交量对收益的影响，可以用于识别具有较高收益潜力且波动性相对较低的股票。
    因子应用场景：
    1. 衡量经波动率调整后的短期价格变动。
    2. 识别具有较高收益潜力且波动性相对较低的股票。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 2. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 3. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], 20)
    # 4. 计算 multiply(ts_std_dev(close, 20), adv(vol,20))
    data_multiply = multiply(data_ts_std_dev, data_adv)
    # 5. 计算 divide(ts_delta(close, 5), multiply(ts_std_dev(close, 20),adv(vol,20)))
    factor = divide(data_ts_delta, data_multiply)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()