import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import sign, ts_delta, multiply

def factor_0011(data, **kwargs):
    """
    数学表达式: (sign(ts_delta(volume, 1)) * (-1 * ts_delta(close, 1)))
    中文描述: 该因子首先计算成交量的每日变化，然后取其符号，再计算收盘价的每日变化并取负数，最后将二者相乘；该因子反映了成交量变化方向与价格变化方向的反向关系，当成交量增加而价格下跌时，因子为正，反之则为负；可以用于识别成交量异动与价格背离的情况，例如，在趋势跟踪策略中，该因子可以作为过滤条件，避免在成交量下降但价格上涨时追高，或者在成交量上升但价格下跌时抄底；也可以用于构建量价组合策略，结合其他量价因子进行选股；此外，还可以用于识别潜在的反转信号，当因子值持续为负时，可能预示着价格即将反弹。
    因子应用场景：
    1. 识别成交量异动与价格背离的情况。
    2. 作为趋势跟踪策略的过滤条件，避免追高或抄底。
    3. 构建量价组合策略，结合其他量价因子进行选股。
    4. 识别潜在的反转信号。
    """
    # 1. 计算 ts_delta(volume, 1)
    data_ts_delta_volume = ts_delta(data['vol'], 1)
    # 2. 计算 sign(ts_delta(volume, 1))
    data_sign_ts_delta_volume = sign(data_ts_delta_volume)
    # 3. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 4. 计算 -1 * ts_delta(close, 1)
    data_neg_ts_delta_close = multiply(-1, data_ts_delta_close)
    # 5. 计算 sign(ts_delta(volume, 1)) * (-1 * ts_delta(close, 1))
    factor = multiply(data_sign_ts_delta_volume, data_neg_ts_delta_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()