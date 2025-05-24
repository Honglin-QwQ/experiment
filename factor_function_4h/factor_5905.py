import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, multiply, ts_delta, sqrt

def factor_5905(data, **kwargs):
    """
    因子名称: Volume_Weighted_Price_Change_Skew_29278
    数学表达式: ts_skewness(multiply(ts_delta(close, 1), sqrt(vol)), 10)
    中文描述: 该因子计算过去10天内，每日收盘价变动与成交量平方根乘积的时间序列偏度。收盘价变动反映了价格的短期波动，而成交量的平方根则对极端成交量进行了平滑处理，使其对价格变动的影响更加稳定。将两者相乘可以视为对每日价格变动进行成交量加权，但权重更加平缓。通过计算这个加权价格变动的偏度，因子旨在捕捉市场在价格上涨或下跌时，平滑后的成交量分布的非对称性。正偏度可能表示价格上涨伴随的成交量（平滑后）更大，而负偏度可能表示价格下跌伴随的成交量（平滑后）更大。这可以用于识别市场情绪和趋势的潜在反转或延续信号。相较于参考因子，创新点在于使用了成交量的平方根进行加权，以减少极端成交量的影响，使因子更加稳健。
    因子应用场景：
    1. 市场情绪识别：通过偏度判断市场上涨或下跌时成交量的分布情况，识别市场情绪。
    2. 趋势反转或延续信号：识别潜在的反转或延续信号。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 2. 计算 sqrt(vol)
    data_sqrt_vol = sqrt(data['vol'])
    # 3. 计算 multiply(ts_delta(close, 1), sqrt(vol))
    data_multiply = multiply(data_ts_delta_close, data_sqrt_vol)
    # 4. 计算 ts_skewness(multiply(ts_delta(close, 1), sqrt(vol)), 10)
    factor = ts_skewness(data_multiply, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()