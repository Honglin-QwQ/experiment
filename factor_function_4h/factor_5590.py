import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, rank, ts_corr

def factor_5590(data, **kwargs):
    """
    因子名称: factor_volume_price_divergence_rank_delta_91201
    数学表达式: ts_delta(rank(ts_corr(ts_delta(log(vol), 1), ts_delta(close, 1), 5)), 2)
    中文描述: 该因子计算成交量对数变化与价格变化的相关性的排名，并计算该排名的二阶差分。创新之处在于使用成交量对数的变化率，而非直接使用成交量，捕捉了成交量变化趋势与价格变化趋势之间的关系。通过排名的差分来识别这种关系的变化趋势。
    应用场景：可用于识别成交量和价格变化趋势之间的背离，例如，当成交量快速上升但价格下跌时，该因子可能预示着趋势的反转。
    """
    import numpy as np
    # 1. 计算 log(vol)
    log_vol = np.log(data['vol'])
    # 2. 计算 ts_delta(log(vol), 1)
    data_ts_delta_log_vol = ts_delta(log_vol, 1)
    # 3. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 4. 计算 ts_corr(ts_delta(log(vol), 1), ts_delta(close, 1), 5)
    data_ts_corr = ts_corr(data_ts_delta_log_vol, data_ts_delta_close, 5)
    # 5. 计算 rank(ts_corr(ts_delta(log(vol), 1), ts_delta(close, 1), 5))
    data_rank = rank(data_ts_corr, 2)
    # 6. 计算 ts_delta(rank(ts_corr(ts_delta(log(vol), 1), ts_delta(close, 1), 5)), 2)
    factor = ts_delta(data_rank, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()