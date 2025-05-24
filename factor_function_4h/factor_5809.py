import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5809(data, **kwargs):
    """
    因子名称: VolumePriceVolatilityRatio_19368
    数学表达式: divide(ts_std_dev(vol, 20), ts_std_dev(close, 20))
    中文描述: 该因子计算过去20天成交量标准差与收盘价标准差的比值。它衡量了成交量的波动性相对于价格波动性的强度。较高的因子值可能表明市场情绪波动较大，成交量变化剧烈，而价格相对稳定，或者价格波动剧烈而成交量相对稳定。这可以用于识别市场情绪与价格走势之间的潜在背离或协同。相较于参考因子，该因子通过直接计算成交量和价格的波动性比率，提供了一个更直观的衡量市场活跃度和价格稳定性的指标，避免了复杂的组合和排名操作，更侧重于捕捉波动性之间的相对关系。
    因子应用场景：
    1. 市场情绪分析：用于识别市场情绪波动较大的时期，例如成交量异常活跃但价格波动不大，可能预示着市场参与者对当前价格存在分歧。
    2. 波动性交易：可以作为波动性交易策略的信号，当成交量波动性远大于价格波动性时，可能存在交易机会。
    3. 风险管理：帮助识别市场风险较高的时期，成交量和价格波动性的剧烈变化可能预示着市场不稳定。
    """
    # 1. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], d = 20)
    # 2. 计算 ts_std_dev(close, 20)
    data_ts_std_dev_close = ts_std_dev(data['close'], d = 20)
    # 3. 计算 divide(ts_std_dev(vol, 20), ts_std_dev(close, 20))
    factor = divide(data_ts_std_dev_vol, data_ts_std_dev_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()