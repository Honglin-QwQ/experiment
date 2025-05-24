import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, ts_corr, ts_std_dev, adv
import pandas as pd
import numpy as np

def factor_6107(data, **kwargs):
    """
    因子名称: Volatility_Volume_Price_Correlation_Decay_24121
    数学表达式: ts_decay_exp_window(ts_corr(ts_std_dev(low, 15), adv(volume, 25), 10), 35, 0.7)
    中文描述: 该因子旨在捕捉最低价波动率与成交量之间的短期相关性，并利用指数衰减加权平均来突出近期相关性的影响。它首先计算过去15天最低价的标准差和过去25天平均成交量之间的10天滚动相关性，然后对这个相关性序列应用35天窗口、衰减因子为0.7的指数衰减加权平均。创新点在于结合了短期波动率、中期成交量和短期相关性，并使用指数衰减来捕捉近期市场动态，同时参考了历史输出中对波动率和成交量的关注，并尝试通过相关性和衰减平均来改进预测能力和稳定性，避免了直接的波动率比率，而是关注它们之间的动态关系。
    因子应用场景：
    1. 市场情绪分析： 用于识别市场中价格波动与成交量之间的关系，特别是在趋势形成或反转时。
    2. 风险管理： 评估资产的波动性与交易活跃度之间的关联，帮助识别潜在的风险。
    3. 交易策略： 结合指数衰减的特性，可以用于制定更侧重近期市场动态的交易策略。
    """
    # 1. 计算 ts_std_dev(low, 15)
    data_ts_std_dev_low = ts_std_dev(data['low'], 15)
    # 2. 计算 adv(volume, 25)
    data_adv_volume = adv(data['vol'], 25)
    # 3. 计算 ts_corr(ts_std_dev(low, 15), adv(volume, 25), 10)
    data_ts_corr = ts_corr(data_ts_std_dev_low, data_adv_volume, 10)
    # 4. 计算 ts_decay_exp_window(ts_corr(ts_std_dev(low, 15), adv(volume, 25), 10), 35, 0.7)
    factor = ts_decay_exp_window(data_ts_corr, 35, 0.7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()