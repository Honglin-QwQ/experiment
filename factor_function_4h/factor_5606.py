import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, log

def factor_5606(data, **kwargs):
    """
    数学表达式: ts_rank(ts_delta(log(amount),3), 120) + ts_rank(ts_delta(close,3), 120) + ts_rank(ts_delta(vol,3), 120)
    中文描述: 该因子是factor_0002的改进版本，在原有的交易额的对数变化率和收盘价的变化率的基础上，加入了成交量的变化率，并分别进行时间序列排名，然后将三个排名相加。
            这一改进旨在同时捕捉市场资金流动、价格趋势和市场活跃度的变化，通过结合三个信息源，提高因子对市场情绪和潜在交易机会的识别能力。
            相较于单一的交易额变化，加入收盘价变化和成交量变化可以更全面地反映市场动态，从而提升因子的预测能力。
    因子应用场景：
    1. 市场情绪捕捉： 通过结合交易额、收盘价和成交量的变化，更全面地反映市场情绪。
    2. 交易机会识别： 提高因子对潜在交易机会的识别能力。
    3. 市场动态反映： 更全面地反映市场动态，提升因子的预测能力。
    """
    # 1. 计算 log(amount)
    log_amount = log(data['amount'])
    # 2. 计算 ts_delta(log(amount),3)
    ts_delta_log_amount = ts_delta(log_amount, 3)
    # 3. 计算 ts_rank(ts_delta(log(amount),3), 120)
    ts_rank_ts_delta_log_amount = ts_rank(ts_delta_log_amount, 120)
    # 4. 计算 ts_delta(close,3)
    ts_delta_close = ts_delta(data['close'], 3)
    # 5. 计算 ts_rank(ts_delta(close,3), 120)
    ts_rank_ts_delta_close = ts_rank(ts_delta_close, 120)
    # 6. 计算 ts_delta(vol,3)
    ts_delta_vol = ts_delta(data['vol'], 3)
    # 7. 计算 ts_rank(ts_delta(vol,3), 120)
    ts_rank_ts_delta_vol = ts_rank(ts_delta_vol, 120)
    # 8. 计算 ts_rank(ts_delta(log(amount),3), 120) + ts_rank(ts_delta(close,3), 120) + ts_rank(ts_delta(vol,3), 120)
    factor = ts_rank_ts_delta_log_amount + ts_rank_ts_delta_close + ts_rank_ts_delta_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()