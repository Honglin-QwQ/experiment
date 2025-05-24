import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_sum, ts_zscore
import pandas as pd

def factor_5636(data, **kwargs):
    """
    因子名称: factor_0006_29515
    数学表达式: ts_zscore(ts_sum(divide(amount,vol),6),66)
    中文描述: 该因子首先计算amount和vol的比值，然后对这个比值进行6日求和，最后计算66日Z-score。该因子的创新点在于将交易额和交易量的比值作为输入，衡量了单位交易量对应的交易额大小，可能反映了市场活跃程度或交易的平均规模。再通过求和与zscore，平滑了短期波动，并标准化了长期趋势。
    因子应用场景：
    1. 市场活跃度分析：用于衡量市场活跃程度或交易的平均规模。
    2. 趋势跟踪：通过平滑短期波动，标准化长期趋势，辅助判断市场趋势。
    """
    # 1. 计算 amount 和 vol 的比值
    amount_over_vol = divide(data['amount'], data['vol'])
    # 2. 对比值进行 6 日求和
    sum_amount_over_vol = ts_sum(amount_over_vol, d=6)
    # 3. 计算 66 日 Z-score
    factor = ts_zscore(sum_amount_over_vol, d=66)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()