import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_sum, if_else, ts_delta, abs, ts_max_diff, kth_element, ts_min_diff

def factor_5663(data, **kwargs):
    """
    数学表达式: ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0), 12) + ts_max_diff(kth_element(vwap, 4, k=1), 14) - ts_min_diff(low, 22)
    中文描述: 该因子结合了三个参考因子的思想，旨在综合评估市场情绪和价格支撑。首先，它计算过去12天收盘价下跌幅度的总和，反映了市场的短期下行压力。然后，加上VWAP在过去14天内的最大差值，衡量价格相对于其加权平均值的波动情况。最后，减去最低价与过去22天内最低价格的差值，评估价格的支撑强度。该因子的创新之处在于将市场情绪、价格波动和支撑强度三个维度结合起来，从而更全面地反映市场状态。
    因子应用场景：
    1. 市场情绪评估：通过计算收盘价下跌幅度总和，评估市场短期下行压力。
    2. 价格波动衡量：通过计算VWAP的最大差值，衡量价格相对于其加权平均值的波动情况。
    3. 支撑强度评估：通过计算最低价与过去最低价格的差值，评估价格的支撑强度。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 2. 计算 if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0)
    data_if_else = if_else(data_ts_delta_close < 0, abs(data_ts_delta_close), 0)
    # 3. 计算 ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0), 12)
    data_ts_sum = ts_sum(data_if_else, 12)
    # 4. 计算 kth_element(vwap, 4, k=1)
    data_kth_element = kth_element(data['vwap'], 4, k=1)
    # 5. 计算 ts_max_diff(kth_element(vwap, 4, k=1), 14)
    data_ts_max_diff = ts_max_diff(data_kth_element, 14)
    # 6. 计算 ts_min_diff(low, 22)
    data_ts_min_diff = ts_min_diff(data['low'], 22)
    # 7. 计算 ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0), 12) + ts_max_diff(kth_element(vwap, 4, k=1), 14) - ts_min_diff(low, 22)
    factor = data_ts_sum + data_ts_max_diff - data_ts_min_diff

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()