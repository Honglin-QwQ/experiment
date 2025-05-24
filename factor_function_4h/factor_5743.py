import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, divide

def factor_5743(data, **kwargs):
    """
    因子名称: VWAPDeltaLowRankRatio_80767
    数学表达式: divide(ts_rank(ts_delta(vwap, 3), 20), ts_rank(ts_delta(low, 3), 20))
    中文描述: 该因子计算了VWAP短期变化的时间序列排名与最低价短期变化的时间序列排名的比值。首先，它计算了过去3天VWAP的差分，反映了VWAP的短期变化。然后，计算这个VWAP变化在过去20天的时间序列排名。同时，计算过去3天最低价的差分，反映了最低价的短期变化，并计算其在过去20天的时间序列排名。最后，将VWAP变化的排名除以最低价变化的排名。这个因子旨在捕捉VWAP的短期变化与最低价的短期变化之间的相对强度，并利用时间序列排名来降低异常值的影响和进行标准化。创新点在于直接比较VWAP和最低价的短期变化排名，构建了排名之间的比值关系，并参考了用户提供的因子改进建议中关于短期变化和排名处理的思路。
    因子应用场景：
    1. 相对强度分析：用于衡量VWAP短期变化相对于最低价短期变化的强度，判断股票是更受成交量驱动还是价格驱动。
    2. 趋势确认：当因子值较高时，可能表明成交量加权平均价的变化更为显著，趋势可能更可靠。
    3. 异常值过滤：通过时间序列排名，降低了极端价格波动对因子值的影响。
    """
    # 1. 计算 ts_delta(vwap, 3)
    data_ts_delta_vwap = ts_delta(data['vwap'], 3)
    # 2. 计算 ts_rank(ts_delta(vwap, 3), 20)
    data_ts_rank_vwap = ts_rank(data_ts_delta_vwap, 20)
    # 3. 计算 ts_delta(low, 3)
    data_ts_delta_low = ts_delta(data['low'], 3)
    # 4. 计算 ts_rank(ts_delta(low, 3), 20)
    data_ts_rank_low = ts_rank(data_ts_delta_low, 20)
    # 5. 计算 divide(ts_rank(ts_delta(vwap, 3), 20), ts_rank(ts_delta(low, 3), 20))
    factor = divide(data_ts_rank_vwap, data_ts_rank_low)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()