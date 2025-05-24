import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_rank, ts_max_diff

def factor_5766(data, **kwargs):
    """
    因子名称: VolumeRank_PriceOscillation_Ratio_86602
    数学表达式: divide(ts_rank(vol, 87), ts_max_diff(close, 77))
    中文描述: 该因子旨在捕捉成交量排名与价格波动幅度之间的关系。它首先计算当前成交量在过去87天内的排名，作为市场活跃度的指标，参考了第一个参考因子。然后，计算当前收盘价与过去77天内最高收盘价的差值，该差值反映了价格从近期高点回落的幅度，参考了第三个参考因子中的ts_min_diff的逻辑并进行了创新性的反向应用。最后，将成交量排名除以价格回落幅度。因子值越高，表示在成交量排名较高（市场活跃）的情况下，价格从近期高点回落的幅度相对较小，可能预示着市场在活跃状态下仍维持相对强势。创新点在于结合了成交量的时间序列排名和价格从近期高点回落的幅度，并通过比率形式构建因子，旨在捕捉市场活跃度和价格波动之间的非线性关系。此因子借鉴了历史输出中比率因子的结构，并对参考因子进行了组合和创新性改造。
    因子应用场景：
    1. 市场活跃度分析：用于识别在成交量排名较高的情况下，价格回落幅度较小的股票，可能预示着市场在活跃状态下仍维持相对强势。
    2. 趋势判断：结合成交量和价格波动，辅助判断市场趋势的强弱。
    """
    # 1. 计算 ts_rank(vol, 87)
    data_ts_rank_vol = ts_rank(data['vol'], d=87)
    # 2. 计算 ts_max_diff(close, 77)
    data_ts_max_diff_close = ts_max_diff(data['close'], d=77)
    # 3. 计算 divide(ts_rank(vol, 87), ts_max_diff(close, 77))
    factor = divide(data_ts_rank_vol, data_ts_max_diff_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()