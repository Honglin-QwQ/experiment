import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import multiply, ts_std_dev, ts_arg_max
import pandas as pd

def factor_5642(data, **kwargs):
    """
    因子名称: MomentumAdjustedVolatility_49228
    数学表达式: multiply(returns, ts_std_dev(returns, 20), ts_arg_max(returns, 10))
    中文描述: 该因子结合了收益率、收益率波动率和短期动量信息。首先计算过去20天收益率的标准差，作为波动率的衡量。然后，使用ts_arg_max找到过去10天内收益率最高点的位置。最后，将当前收益率、波动率和最高收益率位置相乘。该因子旨在捕捉高波动率和近期收益率峰值对当前收益率的影响，可能用于识别具有爆发性增长潜力的股票。
    因子应用场景：
    1. 识别具有爆发性增长潜力的股票。
    2. 衡量高波动率和近期收益率峰值对当前收益率的影响。
    """
    # 1. 计算 ts_std_dev(returns, 20)
    data_ts_std_dev = ts_std_dev(data['returns'], 20)
    # 2. 计算 ts_arg_max(returns, 10)
    data_ts_arg_max = ts_arg_max(data['returns'], 10)
    # 3. 计算 multiply(returns, ts_std_dev(returns, 20), ts_arg_max(returns, 10))
    factor = multiply(data['returns'], data_ts_std_dev, data_ts_arg_max)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()