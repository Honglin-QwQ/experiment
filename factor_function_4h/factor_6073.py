import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_6073(data, **kwargs):
    """
    因子名称: VWAP_Entropy_Jump_Ratio_Ranked_14223
    数学表达式: rank(divide(ts_entropy(vwap, 30), add(jump_decay(vwap, d=15, sensitivity=0.08, force=0.3), 0.001)))
    中文描述: 该因子计算VWAP的短期熵与经过改进的VWAP跳跃衰减值的比率，并对结果进行排名。首先计算过去30天VWAP的时间序列熵，捕捉中短期价格不确定性。然后计算经过参数优化的VWAP跳跃衰减值，该值反映了当前VWAP与过去15天内VWAP的显著跳跃程度，并进行平滑处理，同时加上一个小常数避免除以零。最后，将VWAP的短期熵除以改进后的跳跃衰减值，并对最终结果进行排名。这个因子旨在识别在价格不确定性中等的情况下，价格是否经历了显著的跳跃或趋势变化，并通过排名减少异常值的影响。相较于参考因子，创新点在于调整了熵和跳跃衰减的计算窗口和参数，引入了常数避免除以零，并对最终结果进行了排名，以提高因子的稳定性和鲁棒性。
    因子应用场景：
    1. 价格不确定性分析：用于识别价格波动较大，但同时存在显著跳跃或趋势变化的股票。
    2. 趋势反转预测：该因子可能有助于捕捉趋势反转的早期信号，尤其是在市场不确定性较高时。
    3. 量化交易策略：可作为量化交易策略的输入特征，用于筛选具有潜在投资价值的股票。
    """
    # 1. 计算 ts_entropy(vwap, 30)
    data_ts_entropy = ts_entropy(data['vwap'], 30)
    # 2. 计算 jump_decay(vwap, d=15, sensitivity=0.08, force=0.3)
    data_jump_decay = jump_decay(data['vwap'], d=15, sensitivity=0.08, force=0.3)
    # 3. 计算 add(jump_decay(vwap, d=15, sensitivity=0.08, force=0.3), 0.001)
    data_add = add(data_jump_decay, 0.001)
    # 4. 计算 divide(ts_entropy(vwap, 30), add(jump_decay(vwap, d=15, sensitivity=0.08, force=0.3), 0.001))
    data_divide = divide(data_ts_entropy, data_add)
    # 5. 计算 rank(divide(ts_entropy(vwap, 30), add(jump_decay(vwap, d=15, sensitivity=0.08, force=0.3), 0.001)))
    factor = rank(data_divide, rate = 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()