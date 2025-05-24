import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_min_diff, divide

def factor_5758(data, **kwargs):
    """
    因子名称: VolRank_PriceDiff_Ratio_88208
    数学表达式: divide(ts_rank(vol, 50), ts_min_diff(close, 100))
    中文描述: 该因子结合了交易量的时间序列排名和收盘价与历史最小值的差异。它计算过去50天交易量的排名，并将其除以当前收盘价与过去100天最低收盘价的差值。高交易量排名可能表示市场活跃度高，而收盘价与历史最低价的差值反映了价格从低点反弹的程度。该因子旨在识别在市场活跃度较高且价格已从历史低点反弹的股票，这可能预示着持续的上涨动能。创新点在于将交易量排名与价格反弹程度相结合，通过比率的形式捕捉这两者之间的关系，提供一个更全面的视角来评估市场情绪和价格动能。
    因子应用场景：
    1. 市场活跃度分析：用于识别交易量较高且价格从低点反弹的股票。
    2. 动量交易：寻找具有持续上涨动能的股票。
    """
    # 1. 计算 ts_rank(vol, 50)
    data_ts_rank_vol = ts_rank(data['vol'], 50)
    # 2. 计算 ts_min_diff(close, 100)
    data_ts_min_diff_close = ts_min_diff(data['close'], 100)
    # 3. 计算 divide(ts_rank(vol, 50), ts_min_diff(close, 100))
    factor = divide(data_ts_rank_vol, data_ts_min_diff_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()