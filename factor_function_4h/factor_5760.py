import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_decay_linear, ts_std_dev, ts_delta

def factor_5760(data, **kwargs):
    """
    数学表达式: ts_corr(ts_decay_linear(ts_std_dev(close, 5), 10), ts_delta(low, 1), 20)
    中文描述: 该因子计算短期收盘价标准差的线性衰减值与最低价一日差分之间的长期相关性。它首先捕捉过去5天收盘价的波动性，然后对这个波动性应用10天的线性衰减，以反映近期波动性的重要性逐渐降低。最后，计算这个衰减后的波动性与最低价的日度变化在过去20天内的相关性。该因子旨在识别价格波动模式与最低价趋势之间的关系，可能用于预测价格反转或趋势延续。创新点在于结合了波动性的衰减处理和价格日度变化的长期相关性分析。
    因子应用场景：
    1. 波动性分析：用于分析价格波动性与最低价变化之间的关系。
    2. 趋势预测：可能用于预测价格反转或趋势延续。
    """
    # 1. 计算 ts_std_dev(close, 5)
    data_ts_std_dev_close = ts_std_dev(data['close'], 5)
    # 2. 计算 ts_decay_linear(ts_std_dev(close, 5), 10)
    data_ts_decay_linear = ts_decay_linear(data_ts_std_dev_close, 10)
    # 3. 计算 ts_delta(low, 1)
    data_ts_delta_low = ts_delta(data['low'], 1)
    # 4. 计算 ts_corr(ts_decay_linear(ts_std_dev(close, 5), 10), ts_delta(low, 1), 20)
    factor = ts_corr(data_ts_decay_linear, data_ts_delta_low, 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()