import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_entropy, kth_element, ts_arg_min

def factor_5675(data, **kwargs):
    """
    因子名称: LowPriceEntropyDelta_21950
    数学表达式: ts_delta(ts_entropy(kth_element(low, 5, k=1), 31), ts_arg_min(low, 20))
    中文描述: 该因子是对'ts_entropy(kth_element(low, 5, k=1), 31)'因子的创新。它计算了过去31天内最低价的信息熵，并结合了ts_delta和ts_arg_min。ts_arg_min(low, 20)计算过去20天内最低价出现的位置，然后用ts_delta计算信息熵与最低价位置的差值。这个差值反映了最低价位置变化对价格波动信息量的影响，可以用于识别价格趋势反转的可能性。创新点在于结合了价格波动的信息熵和最低价出现的时间位置，从而更全面地捕捉市场情绪和价格动向。
    因子应用场景：
    1. 趋势反转识别：当因子值出现显著变化时，可能预示着价格趋势即将发生反转。
    2. 市场情绪分析：通过结合价格波动的信息熵和最低价出现的时间位置，更全面地捕捉市场情绪和价格动向。
    """
    # 1. 计算 kth_element(low, 5, k=1)
    data_kth_element = kth_element(data['low'], d=5, k=1)
    # 2. 计算 ts_entropy(kth_element(low, 5, k=1), 31)
    data_ts_entropy = ts_entropy(data_kth_element, d=31)
    # 3. 计算 ts_arg_min(low, 20)
    data_ts_arg_min = ts_arg_min(data['low'], d=20)
    # 4. 计算 ts_delta(ts_entropy(kth_element(low, 5, k=1), 31), ts_arg_min(low, 20))
    factor = ts_delta(data_ts_entropy, d=int(data_ts_arg_min.iloc[-1]))

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()