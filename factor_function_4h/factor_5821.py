import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, ts_arg_max, add, divide, log

def factor_5821(data, **kwargs):
    """
    因子名称: LogDiffHigh_TsArgMaxClose_Ratio_34037
    数学表达式: divide(log_diff(high), add(ts_arg_max(close, 26), 1))
    中文描述: 该因子结合了最高价的对数差分和过去26天收盘价最高点的位置信息。具体计算为最高价的对数差分除以过去26天收盘价最高点出现的相对天数加1。最高价对数差分捕捉了近期价格的相对变化，而收盘价最高点的位置则反映了短期趋势的强度和持续性。通过将两者结合，该因子旨在识别那些近期最高价上涨且短期内收盘价仍接近历史高位的股票，可能预示着持续的上涨动能。分母加1是为了避免除以零的情况，并对近期最高点（相对天数为0）赋予更大的权重。
    因子应用场景：
    1. 趋势跟踪：用于识别价格上涨趋势中的股票。
    2. 动量分析：捕捉价格上涨的动量。
    """
    # 1. 计算 log_diff(high)
    data_log_diff_high = log_diff(data['high'])
    # 2. 计算 ts_arg_max(close, 26)
    data_ts_arg_max_close = ts_arg_max(data['close'], d = 26)
    # 3. 计算 add(ts_arg_max(close, 26), 1)
    data_add_ts_arg_max_close = add(data_ts_arg_max_close, 1)
    # 4. 计算 divide(log_diff(high), add(ts_arg_max(close, 26), 1))
    factor = divide(data_log_diff_high, data_add_ts_arg_max_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()