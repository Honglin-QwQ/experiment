import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear
from operators import ts_returns

def factor_5994(data, **kwargs):
    """
    因子名称: VolumeMomentumDecayIndex_53280
    数学表达式: ts_decay_linear(ts_returns(vol, 22), 10)
    中文描述: 该因子计算过去22天交易量（vol）的相对变化，然后对这个变化序列应用一个10天的线性衰减加权平均。这结合了短期交易量动量和近期数据的更高权重，旨在捕捉交易量变化的持续性和强度，并给予近期交易活动更大的影响力。高因子值可能表明近期交易量持续增长，预示着潜在的市场关注度和流动性提升。
    因子应用场景：
    1. 交易量趋势识别：用于识别交易量持续增长的股票，可能预示着市场关注度提升。
    2. 流动性分析：评估股票的流动性变化，高因子值可能表明流动性增强。
    """
    # 1. 计算 ts_returns(vol, 22)
    data_ts_returns_vol = ts_returns(data['vol'], 22)
    # 2. 计算 ts_decay_linear(ts_returns(vol, 22), 10)
    factor = ts_decay_linear(data_ts_returns_vol, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()