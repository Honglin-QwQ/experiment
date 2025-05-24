import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5993(data, **kwargs):
    """
    因子名称: Vol_Jump_Decay_Skewness_Ratio_13985
    数学表达式: divide(signed_power(jump_decay(ts_median(vol, 77), d=5, sensitivity=0.1, force=0.2), 3), ts_skewness(vol, 60))
    中文描述: 该因子旨在通过结合交易量中位数的衰减跳跃信号和长期交易量偏度，捕捉市场情绪的非对称变化。它首先计算过去77天交易量的中位数（ts_median(vol, 77)）并应用jump_decay操作符来识别和衰减显著的跳跃，然后对衰减后的跳跃信号进行三次幂运算以放大其强度和方向性。最后，将这个经过处理的跳跃信号除以过去60天交易量的偏度（ts_skewness(vol, 60)）。

    因子逻辑:
    1. ts_median(vol, 77) 计算中长期交易活跃度中位数。
    2. jump_decay(...) 检测并衰减交易量中位数序列中的显著跳跃，保留关键变化信息。
    3. signed_power(..., 3) 对衰减后的跳跃信号进行三次幂运算，增强信号的非线性特征，放大正负跳跃的影响。
    4. ts_skewness(vol, 60) 计算过去60天交易量的偏度，反映交易量分布的非对称性，可以作为市场情绪的指标。
    5. divide(...) 将经过处理的跳跃信号与长期交易量偏度相除，旨在捕捉在不同交易量分布形态下，交易量跳跃信号的相对强度。

    创新点:
    该因子创新性地将交易量中位数的衰减跳跃与长期交易量偏度相结合，构建了一个能够反映市场情绪非对称变化的复合信号。通过对跳跃信号进行三次幂运算，增强了因子的非线性特征。与原始因子相比，引入交易量偏度作为分母，使得因子能够根据市场交易量分布的特征来调整跳跃信号的解释，例如在交易量分布偏斜的市场中，同样的交易量跳跃可能具有不同的含义。这有助于提高因子在不同市场环境下的适应性和预测能力。

    应用场景:
    该因子可用于识别那些在交易量中长期趋势发生关键变化时，伴随特定交易量分布特征的资产。例如，在交易量大幅增加（正向跳跃）且交易量分布右偏（正偏度）的市场中，该因子可能捕捉到由积极情绪驱动的上涨机会。反之，在交易量大幅减少（负向跳跃）且交易量分布左偏（负偏度）的市场中，可能预示着下跌风险。该因子适用于需要捕捉市场情绪非对称变化和交易量异常波动的交易策略。
    """
    # 1. 计算 ts_median(vol, 77)
    data_ts_median_vol = ts_median(data['vol'], d=77)
    # 2. 计算 jump_decay(ts_median(vol, 77), d=5, sensitivity=0.1, force=0.2)
    data_jump_decay = jump_decay(data_ts_median_vol, d=5, sensitivity=0.1, force=0.2)
    # 3. 计算 signed_power(jump_decay(ts_median(vol, 77), d=5, sensitivity=0.1, force=0.2), 3)
    data_signed_power = signed_power(data_jump_decay, 3)
    # 4. 计算 ts_skewness(vol, 60)
    data_ts_skewness_vol = ts_skewness(data['vol'], d=60)
    # 5. 计算 divide(signed_power(jump_decay(ts_median(vol, 77), d=5, sensitivity=0.1, force=0.2), 3), ts_skewness(vol, 60))
    factor = divide(data_signed_power, data_ts_skewness_vol)

    # 删除中间变量
    del data_ts_median_vol
    del data_jump_decay
    del data_signed_power
    del data_ts_skewness_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()