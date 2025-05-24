import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_delta, ts_std_dev
import pandas as pd

def factor_5942(data, **kwargs):
    """
    因子名称: VolumePriceVolatilityCorrelation_54299
    数学表达式: ts_corr(ts_delta(close, 5), ts_std_dev(volume, 10), 7)
    中文描述: 该因子旨在捕捉短期价格变化与短期交易量波动之间的相关性。首先计算过去5天的收盘价变化 (ts_delta(close, 5))，然后计算过去10天的交易量标准差 (ts_std_dev(volume, 10))。最后，计算这两者在过去7天内的滚动相关性 (ts_corr(..., ..., 7))。相较于参考因子，创新点在于引入了价格变化作为因子成分，并调整了时间窗口参数，以期捕捉价格和交易量之间更短期的动态关系。较高的正相关性可能表明价格的快速变动伴随着交易量的放大和波动，这可能预示着市场情绪的剧烈变化或趋势的形成。该因子可以用于识别价格趋势的可持续性和潜在的交易机会。
    因子应用场景：
    1. 趋势识别：识别价格趋势的可持续性和潜在的交易机会。
    2. 市场情绪分析：捕捉市场情绪的剧烈变化或趋势的形成。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 2. 计算 ts_std_dev(volume, 10)
    data_ts_std_dev_volume = ts_std_dev(data['vol'], 10)
    # 3. 计算 ts_corr(ts_delta(close, 5), ts_std_dev(volume, 10), 7)
    factor = ts_corr(data_ts_delta_close, data_ts_std_dev_volume, 7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()