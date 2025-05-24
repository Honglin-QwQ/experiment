import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import multiply, ts_delta, ts_quantile

def factor_5619(data, **kwargs):
    """
    因子名称: factor_volume_momentum_quantile_53390
    数学表达式: ts_quantile(multiply(volume, ts_delta(close, 5)), 20)
    中文描述: 该因子结合了成交量和价格变动的信息，首先计算成交量与5日收盘价差的乘积，然后计算这个乘积在过去20天内的分位数。这个因子的创新之处在于它同时考虑了成交量的放大效应和价格的短期动量，并通过分位数来平滑极端值，旨在捕捉成交量放大且价格上涨的股票。适用于识别短期内具有较高上涨潜力的股票。
    因子应用场景：
    1. 短期上涨潜力：用于识别成交量放大且价格上涨的股票，这些股票可能具有较高的短期上涨潜力。
    2. 动量捕捉：通过结合成交量和价格变动，捕捉市场中的短期动量。
    3. 风险控制：使用分位数平滑极端值，降低因子受异常值的影响。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 2. 计算 multiply(volume, ts_delta(close, 5))
    data_multiply = multiply(data['vol'], data_ts_delta_close)
    # 3. 计算 ts_quantile(multiply(volume, ts_delta(close, 5)), 20)
    factor = ts_quantile(data_multiply, 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()