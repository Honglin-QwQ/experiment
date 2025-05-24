import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import arc_tan
from operators import ts_rank
from operators import ts_delta
import pandas as pd

def factor_6088(data, **kwargs):
    """
    因子名称: Delayed_Volume_Delta_Rank_ArcTan_88911
    数学表达式: arc_tan(ts_rank(ts_delta(vol, 5), 90))
    中文描述: 该因子结合了交易量的时间序列变化、排名以及反正切函数。首先，计算过去5天交易量的变化（ts_delta(vol, 5)），捕捉短期交易活跃度的波动。
            然后，将这个交易量变化值在过去90天内进行时间序列排名（ts_rank(..., 90)），以评估当前变化在历史上的相对位置。
            最后，对排名结果应用反正切函数（arc_tan(...)）。反正切函数将排名值映射到一个有限的范围内，有助于压缩数据并可能揭示非线性关系。
            这个因子旨在识别那些近期交易量变化在历史中处于极端位置（高或低排名）的股票，并通过反正切变换提供一个标准化且有界的信号，可用于捕捉市场情绪的短期爆发或衰退。
    因子应用场景：
    1. 交易量分析：识别交易量显著变化的股票。
    2. 市场情绪捕捉：通过反正切函数标准化排名，捕捉市场情绪的短期爆发或衰退。
    """
    # 1. 计算 ts_delta(vol, 5)
    data_ts_delta_vol = ts_delta(data['vol'], d=5)
    # 2. 计算 ts_rank(ts_delta(vol, 5), 90)
    data_ts_rank = ts_rank(data_ts_delta_vol, d=90)
    # 3. 计算 arc_tan(ts_rank(ts_delta(vol, 5), 90))
    factor = arc_tan(data_ts_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()