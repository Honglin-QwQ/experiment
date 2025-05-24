import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_corr, ts_rank, ts_scale

def factor_5628(data, **kwargs):
    """
    因子名称: factor_innovative_vol_price_correlation_26973
    数学表达式: ts_zscore(ts_corr(ts_rank(close, 10), ts_scale(vol, 20), 15), 20)
    中文描述: 该因子旨在捕捉价格和成交量之间的动态关系，并识别异常的相关性模式。首先，对收盘价进行10日排名，以反映价格的相对强度。然后，对成交量进行20日时间序列缩放，使其在0到1之间，从而标准化成交量。接下来，计算排名后的收盘价和缩放后的成交量在过去15天内的相关性。最后，计算该相关性在过去20天内的Z-score，以识别相对于其历史分布的异常相关性。该因子可用于识别价格和成交量之间出现异常相关性的股票，可能指示潜在的交易机会。
    因子应用场景：
    1. 识别价格和成交量之间出现异常相关性的股票。
    2. 可能指示潜在的交易机会。
    """
    # 1. 计算 ts_rank(close, 10)
    data_ts_rank_close = ts_rank(data['close'], d = 10)
    # 2. 计算 ts_scale(vol, 20)
    data_ts_scale_vol = ts_scale(data['vol'], d = 20)
    # 3. 计算 ts_corr(ts_rank(close, 10), ts_scale(vol, 20), 15)
    data_ts_corr = ts_corr(data_ts_rank_close, data_ts_scale_vol, d = 15)
    # 4. 计算 ts_zscore(ts_corr(ts_rank(close, 10), ts_scale(vol, 20), 15), 20)
    factor = ts_zscore(data_ts_corr, d = 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()