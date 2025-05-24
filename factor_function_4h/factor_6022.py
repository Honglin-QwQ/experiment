import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_returns, ts_delta, ts_std_dev

def factor_6022(data, **kwargs):
    """
    因子名称: VolatilityAdjustedDeltaReturns_64075
    数学表达式: divide(ts_returns(ts_delta(close, 3), 5), ts_std_dev(ts_delta(close, 3), 5))
    中文描述: 该因子计算收盘价在3天周期内变动的5天相对变动，并将其除以该变动在过去5天内的标准差。这旨在衡量短期价格动量相对于其自身波动性的表现。因子结合了参考因子1的短期价格动量捕捉能力和参考因子2的波动性衡量概念，通过标准化处理，使得因子更具可比性，减少极端波动对因子值的影响。高因子值可能表明在相对稳定的短期价格变动下，存在较强的动量效应。
    因子应用场景：
    1. 动量交易：用于识别具有较高动量且波动性较低的股票。
    2. 风险调整：用于评估动量策略的风险调整收益。
    3. 选股：用于在特定行业或市场中选择具有较高风险调整动量的股票。
    """
    # 1. 计算 ts_delta(close, 3)
    data_ts_delta = ts_delta(data['close'], d = 3)
    # 2. 计算 ts_returns(ts_delta(close, 3), 5)
    data_ts_returns = ts_returns(data_ts_delta, d = 5)
    # 3. 计算 ts_std_dev(ts_delta(close, 3), 5)
    data_ts_std_dev = ts_std_dev(data_ts_delta, d = 5)
    # 4. 计算 divide(ts_returns(ts_delta(close, 3), 5), ts_std_dev(ts_delta(close, 3), 5))
    factor = divide(data_ts_returns, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()