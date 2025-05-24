import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, jump_decay
import pandas as pd

def factor_5931(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Jump_Decay_81483
    数学表达式: jump_decay(ts_std_dev(vwap, 10), d=5, sensitivity=0.2, force=0.05)
    中文描述: 该因子计算过去10天VWAP的标准差，然后使用jump_decay操作符平滑处理这个标准差序列。jump_decay会识别标准差序列中相对于过去5天数据的显著“跳跃”，并计算一个衰减贡献值来平滑这些跳跃。sensitivity参数控制跳跃的敏感度，force控制衰减的强度。这个因子旨在捕捉VWAP波动率的短期剧烈变化，并通过衰减处理来降低异常波动的影响，从而提供一个更稳定的波动率信号。它可以用于识别市场波动性突然增加或减少的股票，可能预示着潜在的交易机会或风险。
    因子应用场景：
    1. 波动性识别：识别市场波动性突然增加或减少的股票。
    2. 风险管理：评估股票的短期风险水平。
    3. 交易信号：结合其他因子，产生交易信号。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], d=10)
    # 2. 计算 jump_decay(ts_std_dev(vwap, 10), d=5, sensitivity=0.2, force=0.05)
    factor = jump_decay(data_ts_std_dev_vwap, d=5, sensitivity=0.2, force=0.05)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()