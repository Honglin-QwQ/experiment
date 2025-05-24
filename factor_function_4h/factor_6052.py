import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_decay_linear, divide, max, ts_corr, ts_decay_exp_window, adv
import pandas as pd

def factor_6052(data, **kwargs):
    """
    因子名称: VolPriceCorrDecayRatio_60261
    数学表达式: divide(rank(ts_decay_linear(vol, 10)), max(ts_corr(close, open, 10), ts_decay_exp_window(adv(20), 10, factor=0.7)))
    中文描述: 该因子旨在捕捉近期交易量线性衰减排名与价格日内趋势及长期交易量指数衰减之间的相对强度。首先，计算过去10天交易量的线性衰减值并进行排名，赋予近期交易量更高的权重。然后，取过去10天收盘价与开盘价相关性以及过去20天平均交易量的10天指数衰减均值中的最大值。最后，将交易量线性衰减的排名除以这个最大值。相较于历史因子，该因子引入了线性衰减和指数衰减，更精细地捕捉了交易量和价格的动态变化，同时调整了时间窗口，可能更有效地识别市场短期和中期趋势。
    因子应用场景：
    1. 趋势识别：用于识别交易量和价格趋势之间的关系。
    2. 市场情绪：捕捉市场对交易量变化的反应。
    """
    # 1. 计算 ts_decay_linear(vol, 10)
    data_ts_decay_linear = ts_decay_linear(data['vol'], d=10)
    # 2. 计算 rank(ts_decay_linear(vol, 10))
    data_rank = rank(data_ts_decay_linear, rate=2)
    # 3. 计算 adv(20)
    data_adv = adv(data['vol'], d=20)
    # 4. 计算 ts_decay_exp_window(adv(20), 10, factor=0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_adv, d=10, factor=0.7)
    # 5. 计算 ts_corr(close, open, 10)
    data_ts_corr = ts_corr(data['close'], data['open'], d=10)
    # 6. 计算 max(ts_corr(close, open, 10), ts_decay_exp_window(adv(20), 10, factor=0.7))
    data_max = max(data_ts_corr, data_ts_decay_exp_window)
    # 7. 计算 divide(rank(ts_decay_linear(vol, 10)), max(ts_corr(close, open, 10), ts_decay_exp_window(adv(20), 10, factor=0.7)))
    factor = divide(data_rank, data_max)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()