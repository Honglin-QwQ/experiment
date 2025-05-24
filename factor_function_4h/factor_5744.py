import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, rank, ts_corr, ts_delta, ts_min_diff, adv
import pandas as pd

def factor_5744(data, **kwargs):
    """
    数学表达式: subtract(rank(ts_corr(ts_delta(vol, 5), ts_delta(close, 5), 10)), rank(ts_min_diff(ts_delta(adv(vol, 20), 3), 5)))
    中文描述: 该因子在参考因子的基础上进行了创新。它首先计算过去5天成交量差和收盘价差之间在过去10天内的相关性，并对其进行排名。然后，它计算过去20天平均成交量在过去3天内的差值，并找出该差值与过去5天内的最小差值之间的差异，并对其进行排名。最后，用相关性排名的结果减去最小差值差异排名的结果。这个因子的创新点在于结合了成交量和价格的短期变化（通过ts_delta），并引入了ts_min_diff来捕捉平均成交量变化的极端情况。通过比较价量短期变化相关性排名和平均成交量极端变化差异排名的差异，该因子旨在捕捉市场中短期动量和潜在的极端交易行为，可能用于识别趋势的强度或潜在的反转信号。相较于历史输出，该因子引入了ts_delta和ts_min_diff操作符，并改变了相关性和差异的计算基础，以期提高因子的稳定性和预测能力，并解决历史输出中因子值可能全是0的问题。
    因子应用场景：
    1. 趋势识别：因子可以捕捉市场中短期动量和潜在的极端交易行为，可能用于识别趋势的强度或潜在的反转信号。
    2. 反转信号：通过比较价量短期变化相关性排名和平均成交量极端变化差异排名的差异，可能发现潜在的反转信号。
    """
    # 1. 计算 ts_delta(vol, 5)
    data_ts_delta_vol = ts_delta(data['vol'], 5)
    # 2. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 3. 计算 ts_corr(ts_delta(vol, 5), ts_delta(close, 5), 10)
    data_ts_corr = ts_corr(data_ts_delta_vol, data_ts_delta_close, 10)
    # 4. 计算 rank(ts_corr(ts_delta(vol, 5), ts_delta(close, 5), 10))
    factor1 = rank(data_ts_corr, 2)

    # 5. 计算 adv(vol, 20)
    data_adv_vol = adv(data['vol'], 20)
    # 6. 计算 ts_delta(adv(vol, 20), 3)
    data_ts_delta_adv_vol = ts_delta(data_adv_vol, 3)
    # 7. 计算 ts_min_diff(ts_delta(adv(vol, 20), 3), 5)
    data_ts_min_diff = ts_min_diff(data_ts_delta_adv_vol, 5)
    # 8. 计算 rank(ts_min_diff(ts_delta(adv(vol, 20), 3), 5))
    factor2 = rank(data_ts_min_diff, 2)

    # 9. 计算 subtract(rank(ts_corr(ts_delta(vol, 5), ts_delta(close, 5), 10)), rank(ts_min_diff(ts_delta(adv(vol, 20), 3), 5)))
    factor = subtract(factor1, factor2, filter = False)

    # 删除中间变量
    del data_ts_delta_vol
    del data_ts_delta_close
    del data_ts_corr
    del data_adv_vol
    del data_ts_delta_adv_vol
    del data_ts_min_diff
    del factor1
    del factor2

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()