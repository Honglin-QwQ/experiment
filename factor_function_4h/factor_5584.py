import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, signed_power, ts_delta

def factor_5584(data, **kwargs):
    """
    因子名称: factor_0001_54249
    数学表达式: ts_rank(signed_power(ts_delta(high, 1), 2), 20) - ts_rank(signed_power(ts_delta(low, 1), 2), 20)
    中文描述: 该因子通过计算最高价和最低价的差值变化，并进行平方处理，放大了价格波动的影响。然后，分别对最高价和最低价的平方差值进行时间序列排名，并计算二者之差。该因子旨在捕捉价格波动方向和强度的变化，通过最高价和最低价的差异来反映市场情绪，从而辅助判断趋势。
    因子应用场景：
    1. 波动性分析：用于衡量价格波动幅度，数值越大可能表示价格波动越剧烈。
    2. 趋势判断：结合其他因子，辅助判断市场趋势，例如，因子值持续上升可能预示上涨趋势。
    """
    # 1. 计算 ts_delta(high, 1)
    data_ts_delta_high = ts_delta(data['high'], 1)
    # 2. 计算 signed_power(ts_delta(high, 1), 2)
    data_signed_power_high = signed_power(data_ts_delta_high, 2)
    # 3. 计算 ts_rank(signed_power(ts_delta(high, 1), 2), 20)
    data_ts_rank_high = ts_rank(data_signed_power_high, 20)
    # 4. 计算 ts_delta(low, 1)
    data_ts_delta_low = ts_delta(data['low'], 1)
    # 5. 计算 signed_power(ts_delta(low, 1), 2)
    data_signed_power_low = signed_power(data_ts_delta_low, 2)
    # 6. 计算 ts_rank(signed_power(ts_delta(low, 1), 2), 20)
    data_ts_rank_low = ts_rank(data_signed_power_low, 20)
    # 7. 计算 ts_rank(signed_power(ts_delta(high, 1), 2), 20) - ts_rank(signed_power(ts_delta(low, 1), 2), 20)
    factor = data_ts_rank_high - data_ts_rank_low

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()