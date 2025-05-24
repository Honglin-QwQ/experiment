import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, inverse, ts_median, multiply

def factor_5710(data, **kwargs):
    """
    数学表达式: multiply(log_diff(high), inverse(ts_median(vwap, 10)))
    中文描述: 该因子结合了最高价的对数差分和VWAP中位数的倒数。它首先计算日内最高价的对数变化率，以捕捉价格的相对波动。然后，计算过去10天VWAP的中位数，并取其倒数。将这两个值相乘，旨在识别那些近期最高价波动较大，同时过去一段时间内平均交易价格相对较低（中位数倒数较高）的股票。这种组合可能用于寻找价格波动活跃且历史平均交易成本较低的潜在交易机会。创新点在于结合了对数差分和中位数倒数的乘积，从价格波动和历史平均交易成本两个维度进行考量。
    因子应用场景：
    1. 波动性分析：用于识别价格波动较大的股票。
    2. 交易成本评估：结合VWAP中位数倒数，评估历史平均交易成本。
    3. 潜在交易机会：寻找价格波动活跃且历史平均交易成本较低的股票。
    """
    # 1. 计算 log_diff(high)
    data_log_diff_high = log_diff(data['high'])
    # 2. 计算 ts_median(vwap, 10)
    data_ts_median_vwap = ts_median(data['vwap'], 10)
    # 3. 计算 inverse(ts_median(vwap, 10))
    data_inverse_ts_median_vwap = inverse(data_ts_median_vwap)
    # 4. 计算 multiply(log_diff(high), inverse(ts_median(vwap, 10)))
    factor = multiply(data_log_diff_high, data_inverse_ts_median_vwap)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()