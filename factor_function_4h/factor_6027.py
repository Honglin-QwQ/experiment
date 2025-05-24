import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, adv, ts_corr, rank, ts_decay_linear
import pandas as pd

def factor_6027(data, **kwargs):
    """
    因子名称: ts_decay_linear_corr_vol_amount_ratio_rank_19153
    数学表达式: ts_decay_linear(rank(ts_corr(divide(vol, adv(vol, 20)), divide(amount, adv(amount, 20)), 30)), 15)
    中文描述: 该因子首先计算当前成交量与过去20天平均成交量的比值，以及当前交易额与过去20天平均交易额的比值。
            然后，计算这两个比值在过去30天内的相关性。接着，对这个相关性序列进行每日截面排名。
            最后，对这个排名序列进行过去15天的线性衰减加权平均。
            该因子创新点在于：1. 使用了成交量和交易额的相对强度作为输入，更能反映当前交易活动的异常程度；
            2. 计算了这两个相对指标的相关性，捕捉了交易量和交易额之间的协同变化；
            3. 对相关性进行了截面排名，消除了量级差异，更侧重于相对表现；
            4. 对排名进行了线性衰减加权平均，赋予近期表现更高的权重。
            该因子旨在捕捉交易活动强度的相对变化及其与交易额之间的动态关系，并通过排名和衰减加权提高因子的稳定性和预测能力，为识别市场情绪和潜在趋势提供新的视角。
    因子应用场景：
    1. 识别市场情绪：通过成交量和交易额的相对强度及其相关性，辅助判断市场是趋于活跃还是低迷。
    2. 趋势预测：结合线性衰减加权平均，可以帮助识别潜在的趋势反转点。
    3. 量化交易：作为量化交易策略中的一个因子，用于股票选择和仓位管理。
    """
    # 1. 计算 adv(vol, 20)
    adv_vol_20 = adv(data['vol'], d = 20)
    # 2. 计算 divide(vol, adv(vol, 20))
    vol_ratio = divide(data['vol'], adv_vol_20)
    # 3. 计算 adv(amount, 20)
    adv_amount_20 = adv(data['amount'], d = 20)
    # 4. 计算 divide(amount, adv(amount, 20))
    amount_ratio = divide(data['amount'], adv_amount_20)
    # 5. 计算 ts_corr(divide(vol, adv(vol, 20)), divide(amount, adv(amount, 20)), 30)
    corr_vol_amount_ratio = ts_corr(vol_ratio, amount_ratio, d = 30)
    # 6. 计算 rank(ts_corr(divide(vol, adv(vol, 20)), divide(amount, adv(amount, 20)), 30))
    ranked_corr = rank(corr_vol_amount_ratio, rate = 2)
    # 7. 计算 ts_decay_linear(rank(ts_corr(divide(vol, adv(vol, 20)), divide(amount, adv(amount, 20)), 30)), 15)
    factor = ts_decay_linear(ranked_corr, d = 15)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()