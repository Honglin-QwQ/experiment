import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_decay_linear, abs, ts_delta, divide

def factor_5866(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(high, 9), ts_decay_linear(abs(ts_delta(volume, 3)), 9))
    中文描述: 该因子旨在捕捉短期价格波动性与成交量变化动量之间的关系。它计算过去9天最高价的标准差（反映短期价格波动）与过去9天成交量变化绝对值的线性衰减平均值（反映成交量的动量，并对近期变化赋予更高权重）的比率。通过这个比率，因子试图识别价格波动性是否与成交量的持续变化相匹配。高比率可能表明价格波动性在成交量动量减弱的情况下持续存在，反之亦然。创新点在于结合了价格波动性与成交量变化动量，并使用线性衰减平均来强调近期成交量变化的影响，同时利用绝对值捕捉双向的成交量变化。
    因子应用场景：
    1. 波动性确认：用于确认价格波动性是否得到成交量的支持。如果波动性上升但成交量动量减弱，可能表明趋势的可持续性较弱。
    2. 趋势反转信号：当因子值异常高或低时，可能预示着趋势的反转。例如，高波动性但成交量动量减弱可能预示着上涨趋势的结束。
    3. 量价关系分析：用于深入分析量价关系，帮助识别市场中的异常行为和潜在机会。
    """
    # 1. 计算 ts_std_dev(high, 9)
    data_ts_std_dev_high = ts_std_dev(data['high'], d=9)
    # 2. 计算 ts_delta(volume, 3)
    data_ts_delta_volume = ts_delta(data['vol'], d=3)
    # 3. 计算 abs(ts_delta(volume, 3))
    data_abs_ts_delta_volume = abs(data_ts_delta_volume)
    # 4. 计算 ts_decay_linear(abs(ts_delta(volume, 3)), 9)
    data_ts_decay_linear_abs_ts_delta_volume = ts_decay_linear(data_abs_ts_delta_volume, d=9)
    # 5. 计算 divide(ts_std_dev(high, 9), ts_decay_linear(abs(ts_delta(volume, 3)), 9))
    factor = divide(data_ts_std_dev_high, data_ts_decay_linear_abs_ts_delta_volume)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()