import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_6065(data, **kwargs):
    """
    因子名称: VolatilityTrendReversalIndicator_25270
    数学表达式: ts_rank(ts_corr(ts_std_dev(high, 10), ts_delta(low, 5), 10), 15) - rank(ts_co_skewness(vol, close, 15)) + ts_mean(divide(tbase, tquote), 20)
    中文描述: 该因子旨在捕捉价格波动趋势的潜在反转信号，并结合成交量与价格的同步异动以及主动买卖力量。首先，计算过去10天内最高价的标准差与过去5天最低价变化的10天时间序列相关性，并在过去15天内进行时间序列排名，以衡量价格波动与最低价趋势的动态关联强度。其次，计算过去15天内成交量与收盘价的协偏度并进行横截面排名，以识别成交量和价格倾向于同向大幅波动的股票。最后，计算过去20天内主动买入基础币种数量与主动买入计价币种数量比值的平均值，反映市场主动买卖力量的平衡。最终因子为价格波动与最低价趋势相关性排名减去成交量与收盘价协偏度排名，再加上主动买卖力量比值的平均值。创新点在于通过结合高低价波动与最低价趋势的时序相关性排名，更精细地捕捉价格波动趋势的变化，并调整了协偏度和主动买卖力量比值的计算窗口，以期提高因子的预测能力和稳定性。
    因子应用场景：
    1. 反转信号识别：用于识别价格波动趋势可能发生反转的股票。
    2. 市场情绪分析：结合成交量与价格的协偏度，辅助判断市场情绪。
    3. 主动买卖力量评估：通过主动买卖力量比值的平均值，评估市场买卖力量的平衡状态。
    """
    # 1. 计算 ts_std_dev(high, 10)
    data_ts_std_dev = ts_std_dev(data['high'], 10)
    # 2. 计算 ts_delta(low, 5)
    data_ts_delta = ts_delta(data['low'], 5)
    # 3. 计算 ts_corr(ts_std_dev(high, 10), ts_delta(low, 5), 10)
    data_ts_corr = ts_corr(data_ts_std_dev, data_ts_delta, 10)
    # 4. 计算 ts_rank(ts_corr(ts_std_dev(high, 10), ts_delta(low, 5), 10), 15)
    data_ts_rank = ts_rank(data_ts_corr, 15)
    # 5. 计算 ts_co_skewness(vol, close, 15)
    data_ts_co_skewness = ts_co_skewness(data['vol'], data['close'], 15)
    # 6. 计算 rank(ts_co_skewness(vol, close, 15))
    data_rank = rank(data_ts_co_skewness, 2)
    # 7. 计算 divide(tbase, tquote)
    data_divide = divide(data['tbase'], data['tquote'])
    # 8. 计算 ts_mean(divide(tbase, tquote), 20)
    data_ts_mean = ts_mean(data_divide, 20)
    # 9. 计算 ts_rank(ts_corr(ts_std_dev(high, 10), ts_delta(low, 5), 10), 15) - rank(ts_co_skewness(vol, close, 15)) + ts_mean(divide(tbase, tquote), 20)
    factor = data_ts_rank - data_rank + data_ts_mean

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()