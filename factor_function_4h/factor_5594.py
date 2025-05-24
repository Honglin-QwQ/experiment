import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import adv, ts_delta, rank, ts_decay_linear

def factor_5594(data, **kwargs):
    """
    因子名称: factor_volume_momentum_rank_decay_81416
    数学表达式: ts_decay_linear(rank(ts_delta(adv(vol, 5), 10)), d=5)
    中文描述: 该因子旨在捕捉成交量动量的变化趋势，并赋予近期变化更高的权重。首先，计算过去5天平均成交量在10天内的变化量，然后对该变化量进行横截面排名，最后使用线性衰减函数对排名进行加权平均，使得近期的成交量动量变化对因子值的影响更大。该因子可以用于识别成交量持续增加或减少的股票，从而辅助判断股票的潜在上涨或下跌趋势，特别是在短期内成交量变化明显的市场中。
    因子应用场景：
    1. 趋势识别：识别成交量持续增加或减少的股票，辅助判断股票的潜在上涨或下跌趋势。
    2. 短期市场：特别是在短期内成交量变化明显的市场中。
    """
    # 1. 计算 adv(vol, 5)
    data_adv_vol = adv(data['vol'], d=5)
    # 2. 计算 ts_delta(adv(vol, 5), 10)
    data_ts_delta = ts_delta(data_adv_vol, d=10)
    # 3. 计算 rank(ts_delta(adv(vol, 5), 10))
    data_rank = rank(data_ts_delta, rate = 2)
    # 4. 计算 ts_decay_linear(rank(ts_delta(adv(vol, 5), 10)), d=5)
    factor = ts_decay_linear(data_rank, d=5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()