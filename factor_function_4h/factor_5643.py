import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_rank, log, divide, ts_delay, multiply

def factor_5643(data, **kwargs):
    """
    因子名称: factor_0001_82893
    数学表达式: ts_delta(ts_rank(close, d = 5), d = 2) * log(divide(high, ts_delay(low, d = 5)))
    中文描述: 该因子结合了收盘价排名的变化和最高价与过去最低价的比率的对数。首先，计算过去5天收盘价的排名，并计算其2日差分，捕捉收盘价排名变化的动量。然后，计算最高价与5天前最低价的比率的对数，衡量价格波动幅度。最后，将两者相乘，旨在捕捉价格动量与波动率之间的关系。该因子可能用于识别价格快速上涨且波动较大的股票。
    因子应用场景：
    1. 动量捕捉：捕捉收盘价排名变化的动量。
    2. 波动率衡量：衡量价格波动幅度。
    3. 关系识别：识别价格快速上涨且波动较大的股票。
    """
    # 1. 计算 ts_rank(close, d = 5)
    data_ts_rank_close = ts_rank(data['close'], d = 5)
    # 2. 计算 ts_delta(ts_rank(close, d = 5), d = 2)
    data_ts_delta_ts_rank_close = ts_delta(data_ts_rank_close, d = 2)
    # 3. 计算 ts_delay(low, d = 5)
    data_ts_delay_low = ts_delay(data['low'], d = 5)
    # 4. 计算 divide(high, ts_delay(low, d = 5))
    data_divide_high_ts_delay_low = divide(data['high'], data_ts_delay_low)
    # 5. 计算 log(divide(high, ts_delay(low, d = 5)))
    data_log_divide_high_ts_delay_low = log(data_divide_high_ts_delay_low)
    # 6. 计算 ts_delta(ts_rank(close, d = 5), d = 2) * log(divide(high, ts_delay(low, d = 5)))
    factor = multiply(data_ts_delta_ts_rank_close, data_log_divide_high_ts_delay_low)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()