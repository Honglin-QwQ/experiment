import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank
from operators import multiply
from operators import ts_delta
import pandas as pd

def factor_5747(data, **kwargs):
    """
    因子名称: VolWeightedPriceDeltaRank_29850
    数学表达式: ts_rank(multiply(ts_delta(close, 1), vol), 120)
    中文描述: 该因子计算日收盘价变化与成交量的乘积，并将其在过去120天内进行时间序列排名。这结合了价格变动幅度和该变动发生时的市场活跃度。高排名可能表明在交易量活跃的情况下发生了显著的价格变动，这可能预示着趋势的延续或反转。相较于参考因子仅关注成交量或成交量变化，本因子引入了价格变动作为权重，更全面地衡量了市场力量。
    因子应用场景：
    1. 趋势识别：捕捉交易量活跃的情况下发生的显著的价格变动，可能预示着趋势的延续或反转。
    2. 市场力量衡量：通过价格变动作为权重，更全面地衡量了市场力量。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta = ts_delta(data['close'], 1)
    # 2. 计算 multiply(ts_delta(close, 1), vol)
    data_multiply = multiply(data_ts_delta, data['vol'])
    # 3. 计算 ts_rank(multiply(ts_delta(close, 1), vol), 120)
    factor = ts_rank(data_multiply, 120)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()