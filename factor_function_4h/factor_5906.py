import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_min_diff, divide

def factor_5906(data, **kwargs):
    """
    因子名称: VolRank_PriceDiff_Ratio_60350
    数学表达式: divide(ts_rank(vol, 20), ts_min_diff(close, 15))
    中文描述: 该因子结合了成交量的短期排名和收盘价的短期最低价差，旨在衡量当前成交量相对于历史水平的活跃度与当前价格相对于近期支撑位的距离之间的比率。具体来说，它计算过去20天成交量的排名，并将其除以当前收盘价与过去15天最低价的差值。高因子值可能表明在当前价格接近短期支撑位时，成交量异常活跃，这可能预示着潜在的价格反转或趋势加强。创新点在于结合了成交量的时间序列排名和价格与近期支撑位的相对距离，通过比率的形式捕捉市场在特定价格区域的交易情绪和动能。
    因子应用场景：
    1. 潜在反转信号：高因子值可能预示着价格接近支撑位时成交量异常活跃，暗示潜在的反转机会。
    2. 趋势确认：在趋势行情中，因子值持续升高可能表明趋势得到加强。
    3. 交易情绪分析：通过因子值可以了解市场在特定价格区域的交易情绪和动能。
    """
    # 1. 计算 ts_rank(vol, 20)
    data_ts_rank_vol = ts_rank(data['vol'], 20)
    # 2. 计算 ts_min_diff(close, 15)
    data_ts_min_diff_close = ts_min_diff(data['close'], 15)
    # 3. 计算 divide(ts_rank(vol, 20), ts_min_diff(close, 15))
    factor = divide(data_ts_rank_vol, data_ts_min_diff_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()