import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import signed_power, ts_sum, ts_delta

def factor_5599(data, **kwargs):
    """
    因子名称: factor_volume_momentum_53697
    数学表达式: ts_delta(ts_sum(signed_power(volume,2), d = 20), 10)
    中文描述: 该因子结合了成交量的动量和能量的概念。首先，它计算过去20天成交量平方和的时间序列，成交量的平方可以视为一种能量的度量，因为较大的成交量变化会被放大。然后，计算这个能量和的10日差分，捕捉成交量能量变化的趋势。这个因子旨在识别成交量快速累积的股票，这可能预示着潜在的价格动量。
    因子应用场景：
    1. 动量识别：识别成交量快速累积的股票，可能预示着潜在的价格动量。
    2. 趋势跟踪：跟踪成交量能量变化的趋势，辅助判断股票的趋势方向。
    """
    # 1. 计算 signed_power(volume,2)
    data_signed_power = signed_power(data['vol'], 2)
    # 2. 计算 ts_sum(signed_power(volume,2), d = 20)
    data_ts_sum = ts_sum(data_signed_power, d = 20)
    # 3. 计算 ts_delta(ts_sum(signed_power(volume,2), d = 20), 10)
    factor = ts_delta(data_ts_sum, d = 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()