import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_corr, s_log_1p, ts_decay_linear
import numpy as np

def factor_5822(data, **kwargs):
    """
    因子名称: VolPriceCorrelationDecay_67839
    数学表达式: ts_decay_linear(ts_corr(s_log_1p(vol), ((close - open) / ((high - low) + 0.001)), 5), 10)
    中文描述: 该因子旨在捕捉对数变换后的交易量与标准化日内价格波动之间的短期相关性，并应用线性衰减来赋予近期相关性更高的权重。
            表达式首先计算过去5天对数变换后交易量与标准化日内价格波动的滚动相关性，然后对这个相关性序列应用10天的线性衰减。
            创新点在于结合了对数变换平滑交易量、标准化日内价格波动衡量强度以及线性衰减加权近期相关性。
            这可能有助于识别那些近期价量关系变化对未来价格趋势有更强指示作用的股票。
            相较于历史输出，该因子通过引入ts_corr捕捉价量关系，并使用ts_decay_linear强化近期趋势，从而提升了对短期市场动态的敏感度。
    因子应用场景：
    1. 短期趋势判断：用于识别近期价量关系变化对未来价格趋势有更强指示作用的股票。
    2. 市场敏感度分析：用于识别对短期市场动态更敏感的股票。
    """
    # 1. 计算 s_log_1p(vol)
    data_s_log_1p_vol = s_log_1p(data['vol'])
    # 2. 计算 ((close - open) / ((high - low) + 0.001))
    data_price_change = (data['close'] - data['open']) / ((data['high'] - data['low']) + 0.001)
    # 3. 计算 ts_corr(s_log_1p(vol), ((close - open) / ((high - low) + 0.001)), 5)
    data_ts_corr = ts_corr(data_s_log_1p_vol, data_price_change, 5)
    # 4. 计算 ts_decay_linear(ts_corr(s_log_1p(vol), ((close - open) / ((high - low) + 0.001)), 5), 10)
    factor = ts_decay_linear(data_ts_corr, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()