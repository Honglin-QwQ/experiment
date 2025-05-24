import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_corr, ts_delta, log

def factor_5622(data, **kwargs):
    """
    因子名称: factor_volume_price_correlation_18102
    数学表达式: ts_rank(ts_corr(ts_delta(log(close), 1), ts_delta(log(vol), 1), 20), 120)
    中文描述: 该因子计算收盘价对数变化与成交量对数变化之间的相关性，并对该相关性进行时间序列排名。首先，计算收盘价和成交量的对数差分，以捕捉价格和成交量的变化率。然后，计算这两个变化率在过去20天内的相关性。最后，计算该相关性在过去120天内的排名。该因子旨在衡量价格和成交量变化之间的关系强度，并评估该关系在历史上的相对位置。创新点在于结合了价格和成交量的对数变化，以及对相关性进行时间序列排名，从而更全面地捕捉市场动态。
    因子应用场景：
    1. 趋势识别：当因子值较高时，表明收盘价和成交量的相关性较高，可能意味着当前趋势较强且稳定。
    2. 市场同步性分析：因子有助于识别市场中价格变化与成交量同步性较高的股票，这些股票可能对市场整体趋势更为敏感。
    """
    # 1. 计算 log(close)
    log_close = log(data['close'])
    # 2. 计算 log(vol)
    log_vol = log(data['vol'])
    # 3. 计算 ts_delta(log(close), 1)
    delta_log_close = ts_delta(log_close, d = 1)
    # 4. 计算 ts_delta(log(vol), 1)
    delta_log_vol = ts_delta(log_vol, d = 1)
    # 5. 计算 ts_corr(ts_delta(log(close), 1), ts_delta(log(vol), 1), 20)
    corr_delta = ts_corr(delta_log_close, delta_log_vol, d = 20)
    # 6. 计算 ts_rank(ts_corr(ts_delta(log(close), 1), ts_delta(log(vol), 1), 20), 120)
    factor = ts_rank(corr_delta, d = 120)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()