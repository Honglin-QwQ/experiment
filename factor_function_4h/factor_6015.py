import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, adv, ts_corr, ts_decay_linear
import pandas as pd

def factor_6015(data, **kwargs):
    """
    因子名称: ts_corr_returns_vol_ratio_decay_78080
    数学表达式: ts_decay_linear(ts_corr(returns, divide(vol, adv(vol, 10)), 20), 10)
    中文描述: 该因子计算过去20天每日收益率与当前成交量相对于过去10天平均成交量之比的相关性，然后对这个相关性序列进行过去10天的线性衰减加权平均。
    首先，`divide(vol, adv(vol, 10))`计算了当前成交量与过去10天平均成交量的比值，这可以反映当前交易活动的相对强度。
    然后，`ts_corr(returns, ..., 20)`计算了每日收益率与这个相对成交量比值在过去20天内的相关性，捕捉了价格变动与交易活跃度之间的关系。
    最后，`ts_decay_linear(..., 10)`对这个相关性序列进行线性衰减加权平均，给予近期相关性更高的权重，以反映市场动态的变化。
    该因子创新点在于结合了相对成交量指标和线性衰减加权相关性，旨在捕捉价格与交易活跃度之间动态变化的短期关系，为识别市场情绪和潜在趋势提供新的视角。
    相较于简单的收益率或成交量因子，它更侧重于两者之间的协同作用及其随时间的演变。
    因子应用场景：
    1. 市场情绪识别：可用于识别市场情绪与交易活跃度之间的关系，例如，当收益率与相对成交量比值呈现正相关时，可能表明市场情绪乐观。
    2. 趋势跟踪：通过线性衰减加权平均，该因子能够更灵敏地反映近期市场动态，辅助趋势跟踪。
    """

    # 1. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], d = 10)

    # 2. 计算 divide(vol, adv(vol, 10))
    data_divide_vol_adv_vol = divide(data['vol'], data_adv_vol)

    # 3. 计算 ts_corr(returns, divide(vol, adv(vol, 10)), 20)
    data_ts_corr = ts_corr(data['returns'], data_divide_vol_adv_vol, d = 20)

    # 4. 计算 ts_decay_linear(ts_corr(returns, divide(vol, adv(vol, 10)), 20), 10)
    factor = ts_decay_linear(data_ts_corr, d = 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()