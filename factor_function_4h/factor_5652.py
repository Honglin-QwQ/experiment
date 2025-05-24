import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_rank, log, divide, ts_delay, sign, multiply

def factor_5652(data, **kwargs):
    """
    因子名称: factor_0002_72954
    数学表达式: multiply(ts_delta(ts_rank(close, d = 3), d = 1), log(divide(high, ts_delay(low, d = 3))), sign(ts_delta(vol, d = 3)))
    中文描述: 该因子旨在捕捉价格动量、波动率和成交量变化之间的关系。它改进了历史因子，通过引入成交量变化的方向来增强其信号。首先，计算过去3天收盘价的排名，并计算其1日差分，捕捉收盘价排名变化的动量。然后，计算最高价与3天前最低价的比率的对数，衡量价格波动幅度。最后，计算过去3天成交量变化的符号，表示成交量是增加还是减少。将三者相乘，旨在捕捉价格动量与波动率之间的关系，并根据成交量的变化方向进行调整。当价格快速上涨且波动较大，同时成交量增加时，因子值为正，反之为负。这可能用于识别价格趋势的可持续性，成交量增加可能预示着趋势的加强。
    因子应用场景：
    1. 趋势识别：用于识别价格趋势的可持续性，成交量增加可能预示着趋势的加强。
    2. 动量捕捉：捕捉价格动量与波动率之间的关系，并根据成交量的变化方向进行调整。
    """
    # 1. 计算 ts_rank(close, d = 3)
    data_ts_rank_close = ts_rank(data['close'], d = 3)
    # 2. 计算 ts_delta(ts_rank(close, d = 3), d = 1)
    data_ts_delta_ts_rank_close = ts_delta(data_ts_rank_close, d = 1)
    del data_ts_rank_close
    # 3. 计算 ts_delay(low, d = 3)
    data_ts_delay_low = ts_delay(data['low'], d = 3)
    # 4. 计算 divide(high, ts_delay(low, d = 3))
    data_divide_high_ts_delay_low = divide(data['high'], data_ts_delay_low)
    del data_ts_delay_low
    # 5. 计算 log(divide(high, ts_delay(low, d = 3)))
    data_log_divide_high_ts_delay_low = log(data_divide_high_ts_delay_low)
    del data_divide_high_ts_delay_low
    # 6. 计算 ts_delta(vol, d = 3)
    data_ts_delta_vol = ts_delta(data['vol'], d = 3)
    # 7. 计算 sign(ts_delta(vol, d = 3))
    data_sign_ts_delta_vol = sign(data_ts_delta_vol)
    del data_ts_delta_vol
    # 8. 计算 multiply(ts_delta(ts_rank(close, d = 3), d = 1), log(divide(high, ts_delay(low, d = 3))), sign(ts_delta(vol, d = 3)))
    factor = multiply(data_ts_delta_ts_rank_close, data_log_divide_high_ts_delay_low, data_sign_ts_delta_vol)
    del data_ts_delta_ts_rank_close, data_log_divide_high_ts_delay_low, data_sign_ts_delta_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()