import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5837(data, **kwargs):
    """
    数学表达式: ts_corr(ts_decay_exp_window(ts_delta(vwap, 3), d=7, factor=0.7), ts_decay_exp_window(ts_std_dev(vwap, 5), d=15, factor=0.9), 25)
    中文描述: 该因子旨在捕捉VWAP的短期动量（3日变化）与中期波动率（5日标准差）之间的动态相互作用，并引入指数衰减加权，以更强调近期数据的影响。参考了ts_delay和ts_max_diff对VWAP的关注，以及round(close)中对价格行为的捕捉。创新点在于：1. 使用ts_decay_exp_window对动量和波动率进行加权平滑，赋予近期数据更高的权重，增强对市场最新变化的敏感性。2. 调整了ts_delta和ts_std_dev的时间窗口，并增加了ts_corr的计算窗口，以探索不同时间尺度上的关系。3. 通过计算加权动量和加权波动率之间的相关性，试图识别市场情绪和趋势的更深层次信号，例如动量加速伴随波动率上升可能预示趋势的加强，而动量减弱伴随波动率上升可能预示着不确定性和潜在反转。这为投资者提供了一个结合近期动量和风险的更精细视角，有望提升因子的预测能力和稳定性。
    因子应用场景：
    1. 动量与波动率分析：识别动量加速与波动率上升的组合，可能预示趋势加强。
    2. 市场情绪识别：通过动量和波动率的相互作用，洞察市场情绪的微妙变化。
    3. 风险管理：评估动量减弱伴随波动率上升的风险，及时调整投资组合。
    """
    # 1. 计算 ts_delta(vwap, 3)
    data_ts_delta_vwap = ts_delta(data['vwap'], d=3)
    # 2. 计算 ts_decay_exp_window(ts_delta(vwap, 3), d=7, factor=0.7)
    data_ts_decay_exp_window_momentum = ts_decay_exp_window(data_ts_delta_vwap, d=7, factor=0.7)
    # 3. 计算 ts_std_dev(vwap, 5)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], d=5)
    # 4. 计算 ts_decay_exp_window(ts_std_dev(vwap, 5), d=15, factor=0.9)
    data_ts_decay_exp_window_volatility = ts_decay_exp_window(data_ts_std_dev_vwap, d=15, factor=0.9)
    # 5. 计算 ts_corr(ts_decay_exp_window(ts_delta(vwap, 3), d=7, factor=0.7), ts_decay_exp_window(ts_std_dev(vwap, 5), d=15, factor=0.9), 25)
    factor = ts_corr(data_ts_decay_exp_window_momentum, data_ts_decay_exp_window_volatility, d=25)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()