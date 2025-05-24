import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_rank, adv, ts_min_diff

def factor_6013(data, **kwargs):
    """
    因子名称: VolRank_MinDiff_Ratio_51604
    数学表达式: divide(ts_rank(adv(vol, 20), 23), ts_min_diff(open, 48))
    中文描述: 该因子结合了成交量排名和开盘价最小差值两个维度。它计算过去20天平均成交量在过去23天内的排名，并将其除以当前开盘价与过去48天最低开盘价的差值。该因子旨在捕捉市场流动性和价格波动之间的关系。较高的因子值可能表明当前成交量排名较高，但开盘价相对于近期最低点并没有显著上涨，这可能暗示着一种潜在的背离或者市场情绪的复杂性。创新点在于将时间序列排名与时间序列差值运算相结合，并通过除法构建了新的关系，试图捕捉更深层次的市场动态。
    因子应用场景：
    1. 流动性分析：评估成交量排名与价格波动之间的关系，辅助判断市场流动性。
    2. 背离识别：寻找成交量排名较高但价格上涨不明显的股票，可能存在潜在背离。
    3. 市场情绪判断：结合成交量和价格信息，辅助判断市场情绪的复杂性。
    """
    # 1. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], d = 20)
    # 2. 计算 ts_rank(adv(vol, 20), 23)
    data_ts_rank = ts_rank(data_adv, d = 23)
    # 3. 计算 ts_min_diff(open, 48)
    data_ts_min_diff = ts_min_diff(data['open'], d = 48)
    # 4. 计算 divide(ts_rank(adv(vol, 20), 23), ts_min_diff(open, 48))
    factor = divide(data_ts_rank, data_ts_min_diff)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()