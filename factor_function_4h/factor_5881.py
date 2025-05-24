import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, add, ts_rank, ts_min_max_diff
import pandas as pd

def factor_5881(data, **kwargs):
    """
    因子名称: ts_min_max_diff_vol_rank_ratio_43904
    数学表达式: divide(ts_min_max_diff(vol, 116, f=0.85), add(ts_rank(vol, 5), 1))
    中文描述: 该因子计算了交易量在较长周期（116天）内的极值差异（最大值减去最小值乘以0.85倍）与交易量在短期（5天）内的排名（加1以避免除以零）的比值。分子捕捉了较长时间内交易量的波动范围，分母反映了短期内交易量的相对活跃程度。该因子旨在衡量长期交易量波动与短期交易量活跃度的相对关系，可能用于识别在长期波动中短期交易量异常活跃或低迷的情况，从而辅助判断市场情绪和潜在的价格动能。创新点在于结合了长期极值差异和短期排名，并使用比值关系来量化这种相对强度。
    因子应用场景：
    1. 波动率分析：用于衡量长期交易量波动与短期交易量活跃度的相对关系。
    2. 市场情绪判断：辅助判断市场情绪和潜在的价格动能。
    """
    # 1. 计算 ts_min_max_diff(vol, 116, f=0.85)
    data_ts_min_max_diff = ts_min_max_diff(data['vol'], d=116, f=0.85)
    # 2. 计算 ts_rank(vol, 5)
    data_ts_rank = ts_rank(data['vol'], d=5)
    # 3. 计算 add(ts_rank(vol, 5), 1)
    data_add = add(data_ts_rank, 1)
    # 4. 计算 divide(ts_min_max_diff(vol, 116, f=0.85), add(ts_rank(vol, 5), 1))
    factor = divide(data_ts_min_max_diff, data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()