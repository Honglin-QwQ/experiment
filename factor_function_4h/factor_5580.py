import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import multiply, ts_delta, ts_std_dev, ts_zscore, ts_min_diff

def factor_5580(data, **kwargs):
    """
    因子名称: factor_price_volatility_momentum_86311
    数学表达式: multiply(close, ts_delta(ts_std_dev(high, 5), 3), ts_zscore(ts_min_diff(low, 5), 3))
    中文描述: 该因子融合了价格、波动率和动量信息，旨在捕捉短期价格异动。首先，使用ts_std_dev(high, 5)计算过去5天最高价的标准差，反映价格波动率；然后，使用ts_delta(..., 3)计算波动率的3日变化，捕捉波动率的动量；同时，使用ts_min_diff(low, 5)计算最低价与过去5天最低价的差值，反映价格支撑力度；再使用ts_zscore(..., 3)计算该差值的3日Z-score，标准化价格支撑动量。最后，将收盘价、波动率动量和标准化价格支撑动量相乘，得到最终因子值。该因子适用于短线交易，可用于识别潜在的价格反转或突破机会。
    因子应用场景：
    1. 短线交易：识别潜在的价格反转或突破机会。
    2. 波动率分析：捕捉价格波动率的动量变化。
    3. 动量策略：结合价格支撑动量进行交易决策。
    """
    # 1. 计算 ts_std_dev(high, 5)
    data_ts_std_dev = ts_std_dev(data['high'], 5)
    # 2. 计算 ts_delta(ts_std_dev(high, 5), 3)
    data_ts_delta = ts_delta(data_ts_std_dev, 3)
    # 3. 计算 ts_min_diff(low, 5)
    data_ts_min_diff = ts_min_diff(data['low'], 5)
    # 4. 计算 ts_zscore(ts_min_diff(low, 5), 3)
    data_ts_zscore = ts_zscore(data_ts_min_diff, 3)
    # 5. 计算 multiply(close, ts_delta(ts_std_dev(high, 5), 3), ts_zscore(ts_min_diff(low, 5), 3))
    factor = multiply(data['close'], data_ts_delta, data_ts_zscore)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()