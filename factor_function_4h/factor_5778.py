import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5778(data, **kwargs):
    """
    因子名称: VolWeightedPriceMomentum_17605
    数学表达式: multiply(ts_decay_linear(multiply(ts_delta(close, 5), vol), 10), rank(ts_sum(vol, 20)))
    中文描述: 该因子旨在捕捉基于交易量的短期价格动量，并结合长期成交量趋势进行加权。首先，计算过去5天收盘价变化的差值，并乘以当日的交易量，得到一个反映带交易量的短期价格变化的指标。然后，对这个指标进行10天线性衰减加权平均，赋予近期变化更大的权重。最后，将这个加权平均值乘以过去20天总交易量的排名。这种结构创新在于将短期带量价格变化与长期成交量排名相结合，试图识别那些在近期有量价配合上涨或下跌，且长期交易活跃度较高的股票。这可以用于构建短期动量或反转策略，并考虑了市场的流动性因素。
    因子应用场景：
    1. 短期动量策略：识别近期量价齐升的股票，作为潜在的买入对象。
    2. 反转策略：寻找近期量价背离，但长期交易活跃的股票，作为潜在的卖出或反向操作对象。
    3. 流动性风险评估：结合成交量排名，可以评估动量策略的流动性风险，避免选择交易不活跃的股票。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], d=5)
    # 2. 计算 multiply(ts_delta(close, 5), vol)
    data_multiply_delta_vol = multiply(data_ts_delta_close, data['vol'])
    # 3. 计算 ts_decay_linear(multiply(ts_delta(close, 5), vol), 10)
    data_ts_decay_linear = ts_decay_linear(data_multiply_delta_vol, d=10)
    # 4. 计算 ts_sum(vol, 20)
    data_ts_sum_vol = ts_sum(data['vol'], d=20)
    # 5. 计算 rank(ts_sum(vol, 20))
    data_rank_ts_sum_vol = rank(data_ts_sum_vol)
    # 6. 计算 multiply(ts_decay_linear(multiply(ts_delta(close, 5), vol), 10), rank(ts_sum(vol, 20)))
    factor = multiply(data_ts_decay_linear, data_rank_ts_sum_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()