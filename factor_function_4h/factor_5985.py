import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import jump_decay
from operators import ts_median
import pandas as pd

def factor_5985(data, **kwargs):
    """
    因子名称: Vol_Median_Jump_Decay_63420
    数学表达式: jump_decay(ts_median(vol, 77), d=5, sensitivity=0.1, force=0.2)
    中文描述: 该因子旨在捕捉交易量中位数的短期显著跳跃，并通过衰减函数平滑这些跳跃的影响。它首先计算过去77天交易量的中位数（ts_median(vol, 77)），代表中长期的交易活跃度水平。然后，使用jump_decay操作符来识别和处理这个中位数序列中的显著变化（跳跃）。

    因子逻辑:
    1. ts_median(vol, 77) 计算的是过去77天交易量的中位数，用于平滑短期波动，反映中长期交易活跃度。
    2. jump_decay(x, d, sensitivity, force) 操作符检测当前中位数与过去d天中位数之间的显著差异（跳跃），并根据sensitivity和force参数对这些跳跃进行衰减处理。这有助于在保留重要变化信息的同时，降低异常跳跃的瞬时影响。

    创新点:
    该因子创新性地将中位数平滑与跳跃衰减技术结合，旨在更稳健地捕捉交易量中长期趋势中的关键变化点。相较于简单的差分或标准差计算，jump_decay可以更好地处理非线性的、突发性的交易量变化，并且通过参数控制衰减的敏感度和强度，提供了更灵活的信号处理方式。

    应用场景:
    该因子可用于识别交易量中长期趋势的潜在转折点或加速期，尤其适用于那些交易量变化具有突发性特征的资产。通过捕捉经过衰减处理的交易量中位数跳跃，投资者可以获得更平滑但仍能反映重要变化的信号，用于辅助交易决策。
    """
    # 1. 计算 ts_median(vol, 77)
    data_ts_median = ts_median(data['vol'], d=77)
    # 2. 计算 jump_decay(ts_median(vol, 77), d=5, sensitivity=0.1, force=0.2)
    factor = jump_decay(data_ts_median, d=5, sensitivity=0.1, force=0.2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()