import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_6078(data, **kwargs):
    """
    因子名称: VolatilityAdjustedVolumeFlow_Improved_47901
    数学表达式: reverse(ts_decay_exp_window(divide(subtract(tbase, tquote), add(vol, 1e-6)), d=21, factor=0.8)) * ts_std_dev(returns, d=15)
    中文描述: 该因子是基于对先前因子'VolatilityAdjustedVolumeFlow'评估结果的改进。核心逻辑仍然是捕捉基于主动买卖量差异的成交量流，并根据近期收益率的波动性进行调整。
    首先，它计算主动买入量（tbase）与主动卖出量（tquote）的差值，并除以总成交量（vol），得到一个衡量买卖压力的指标。为了避免除以零，总成交量加上一个微小常数1e-6。
    然后，使用指数衰减加权平均（ts_decay_exp_window）对这个买卖压力指标进行平滑处理。根据历史评估结果，我们将窗口期d从11调整为21，衰减因子factor从0.7调整为0.8，以尝试捕捉更长期且平滑的买卖压力趋势。
    接着，将平滑后的买卖压力指标乘以过去15天的收益率标准差（ts_std_dev(returns, d=15)），这里将波动率的窗口期从11调整为15，以与买卖压力的窗口期有所区分，并探索不同的时间尺度组合。
    最后，根据历史评估中因子与未来收益率呈现负相关的结论，我们对整个因子表达式使用了`reverse`操作符进行取反，以期将因子的预测方向调整为正相关。

    创新点：
    1. 在原有主动买卖量差异和总成交量结合的基础上，根据历史评估结果，调整了指数衰减加权平均的窗口期和衰减因子，以优化平滑效果。
    2. 调整了收益率标准差的计算窗口期，探索不同时间尺度下的风险调整效果。
    3. 关键改进是根据历史评估结果，对整个因子表达式进行了`reverse`取反操作，直接修正了预测方向与预期的偏差。

    应用场景：该因子旨在识别在不同波动性环境下，由主动买卖行为驱动的价格动量或反转机会，并通过取反操作，使其信号方向与未来收益率预期一致，适用于捕捉正向的价格趋势。
    """
    # 1. subtract(tbase, tquote)
    data_subtract = subtract(data['tbase'], data['tquote'])

    # 2. add(vol, 1e-6)
    data_add = add(data['vol'], 1e-6)

    # 3. divide(subtract(tbase, tquote), add(vol, 1e-6))
    data_divide = divide(data_subtract, data_add)

    # 4. ts_decay_exp_window(divide(subtract(tbase, tquote), add(vol, 1e-6)), d=21, factor=0.8)
    data_ts_decay_exp_window = ts_decay_exp_window(data_divide, d=21, factor=0.8)

    # 5. ts_std_dev(returns, d=15)
    data_ts_std_dev = ts_std_dev(data['returns'], d=15)

    # 6. reverse(ts_decay_exp_window(divide(subtract(tbase, tquote), add(vol, 1e-6)), d=21, factor=0.8)) * ts_std_dev(returns, d=15)
    factor = reverse(data_ts_decay_exp_window) * data_ts_std_dev

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()