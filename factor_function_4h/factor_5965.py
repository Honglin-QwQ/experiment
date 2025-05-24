import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, rank, ts_zscore, ts_std_dev, jump_decay
import pandas as pd

def factor_5965(data, **kwargs):
    """
    因子名称: VolJumpDecayRankDiff_52628
    数学表达式: subtract(rank(ts_zscore(ts_std_dev(open, 10), 15)), rank(jump_decay(ts_std_dev(open, 10), d=7, sensitivity=0.7, force=0.1)))
    中文描述: 该因子在参考历史因子的基础上进行了创新和改进，旨在更有效地捕捉开盘价波动率的动态变化和潜在的市场情绪突变。首先，它计算过去10天开盘价的标准差（ts_std_dev(open, 10)），作为衡量短期开盘价波动率的基础。然后，对该波动率序列计算过去15天内的Z-Score（ts_zscore(..., 15)），并对其进行排名（rank(...)）。同时，使用jump_decay操作符（d=7, sensitivity=0.7, force=0.1）来平滑和捕捉开盘价波动率序列中的“跳跃”或显著变化，并对其进行排名（rank(...)）。最后，计算波动率Z-Score排名与jump_decay处理后的波动率排名之间的差值。这个差值反映了经过标准化和跳跃衰减处理后的波动率在截面上的相对强弱。相较于原始因子，本因子通过引入jump_decay操作符并计算两个排名之间的差值，期望能更精细地捕捉波动率的突变，并将其与标准化后的波动率进行对比，从而提升因子的预测能力和稳定性，特别是在市场波动加剧或趋势反转初期。改进建议中提到的调整参数、改变因子表达式结构和使用rank操作符等都被采纳。通过计算排名的差值，因子能够更好地反映相对强弱，减少极端值的影响，提高鲁棒性。
    因子应用场景：
    1. 波动率突变捕捉： 因子值可以帮助识别开盘价波动率的显著变化，尤其是在市场波动加剧或趋势反转初期。
    2. 市场情绪分析： 因子值可以反映市场情绪的突变，帮助判断市场风险。
    """
    # 1. 计算 ts_std_dev(open, 10)
    data_ts_std_dev_open = ts_std_dev(data['open'], d=10)
    # 2. 计算 ts_zscore(ts_std_dev(open, 10), 15)
    data_ts_zscore = ts_zscore(data_ts_std_dev_open, d=15)
    # 3. 计算 rank(ts_zscore(ts_std_dev(open, 10), 15))
    rank_zscore = rank(data_ts_zscore, rate = 2)
    # 4. 计算 jump_decay(ts_std_dev(open, 10), d=7, sensitivity=0.7, force=0.1)
    data_jump_decay = jump_decay(data_ts_std_dev_open, d=7, sensitivity=0.7, force=0.1)
    # 5. 计算 rank(jump_decay(ts_std_dev(open, 10), d=7, sensitivity=0.7, force=0.1))
    rank_jump_decay = rank(data_jump_decay, rate = 2)
    # 6. 计算 subtract(rank(ts_zscore(ts_std_dev(open, 10), 15)), rank(jump_decay(ts_std_dev(open, 10), d=7, sensitivity=0.7, force=0.1)))
    factor = subtract(rank_zscore, rank_jump_decay, filter = False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()