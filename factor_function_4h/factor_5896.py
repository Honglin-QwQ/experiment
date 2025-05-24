import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, add, ts_rank, ts_min_max_diff
import pandas as pd

def factor_5896(data, **kwargs):
    """
    因子名称: ts_min_max_diff_vol_rank_ratio_improved_17389
    数学表达式: divide(ts_min_max_diff(vol, 20, f=0.75), add(ts_rank(vol, 5), 1))
    中文描述: 该因子是基于用户提供的原始因子的改进版本。它计算了交易量在较短周期（20天）内的极值差异（最大值减去最小值乘以0.75倍）与交易量在短期（5天）内的排名（加1以避免除以零）的比值。相较于原始因子，我们将ts_min_max_diff的时间窗口从116天缩短到20天，并调整了f参数至0.75，以更敏感地捕捉短期交易量波动。分母的ts_rank(vol, 5)反映了短期内交易量的相对活跃程度。该因子旨在衡量短期交易量波动与短期交易量活跃度的相对关系，可能用于识别在短期波动中交易量异常活跃或低迷的情况，从而辅助判断市场情绪和潜在的价格动能。创新点在于通过调整参数，使因子更专注于短期市场动态，并保留了长期极值差异与短期排名的比值结构。
    因子应用场景：
    1. 短期波动识别：用于识别短期交易量波动与短期交易量活跃度的相对关系。
    2. 市场情绪判断：辅助判断市场情绪和潜在的价格动能。
    """
    # 1. 计算 ts_min_max_diff(vol, 20, f=0.75)
    data_ts_min_max_diff = ts_min_max_diff(data['vol'], d=20, f=0.75)
    # 2. 计算 ts_rank(vol, 5)
    data_ts_rank = ts_rank(data['vol'], d=5)
    # 3. 计算 add(ts_rank(vol, 5), 1)
    data_add = add(data_ts_rank, 1)
    # 4. 计算 divide(ts_min_max_diff(vol, 20, f=0.75), add(ts_rank(vol, 5), 1))
    factor = divide(data_ts_min_max_diff, data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()