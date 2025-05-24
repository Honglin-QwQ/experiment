import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_delta, ts_sum, multiply, add

def factor_5934(data, **kwargs):
    """
    因子名称: VolumeWeightedPriceChangeRatio_32910
    数学表达式: divide(ts_delta(divide(ts_sum(multiply(close, vol), 20), ts_sum(vol, 20)), 5), add(ts_delta(divide(ts_sum(multiply(close, vol), 90), ts_sum(vol, 90)), 10), 0.0001))
    中文描述: 该因子计算短期成交量加权平均收盘价变化率与长期成交量加权平均收盘价变化率的比值。具体来说，它计算过去20天成交量加权平均收盘价的5天变化率，并除以过去90天成交量加权平均收盘价的10天变化率（为避免除以零，分母加了一个小的常数）。这个比值反映了短期和长期价格变化率的相对强度。相较于原始因子，它通过计算变化率的比值，更能捕捉价格变化的相对动能，并且采用了非对称的时间窗口（短期窗口更短，长期窗口更长），以更强调近期数据的影响。这可能有助于识别价格趋势的加速或减速，尤其在震荡市和趋势反转时可能更有效。
    因子应用场景：
    1. 趋势识别：用于识别短期和长期价格变化率的相对强度，判断价格趋势的加速或减速。
    2. 市场反转信号：在震荡市和趋势反转时可能更有效，捕捉价格变化的相对动能。
    """
    # 1. 计算 multiply(close, vol)
    data_multiply = multiply(data['close'], data['vol'])
    # 2. 计算 ts_sum(multiply(close, vol), 20)
    data_ts_sum_short_multiply = ts_sum(data_multiply, 20)
    # 3. 计算 ts_sum(vol, 20)
    data_ts_sum_short_vol = ts_sum(data['vol'], 20)
    # 4. 计算 divide(ts_sum(multiply(close, vol), 20), ts_sum(vol, 20))
    data_divide_short = divide(data_ts_sum_short_multiply, data_ts_sum_short_vol)
    # 5. 计算 ts_delta(divide(ts_sum(multiply(close, vol), 20), ts_sum(vol, 20)), 5)
    data_ts_delta_short = ts_delta(data_divide_short, 5)

    # 6. 计算 ts_sum(multiply(close, vol), 90)
    data_ts_sum_long_multiply = ts_sum(data_multiply, 90)
    # 7. 计算 ts_sum(vol, 90)
    data_ts_sum_long_vol = ts_sum(data['vol'], 90)
    # 8. 计算 divide(ts_sum(multiply(close, vol), 90), ts_sum(vol, 90))
    data_divide_long = divide(data_ts_sum_long_multiply, data_ts_sum_long_vol)
    # 9. 计算 ts_delta(divide(ts_sum(multiply(close, vol), 90), ts_sum(vol, 90)), 10)
    data_ts_delta_long = ts_delta(data_divide_long, 10)

    # 10. 计算 add(ts_delta(divide(ts_sum(multiply(close, vol), 90), ts_sum(vol, 90)), 10), 0.0001)
    data_add = add(data_ts_delta_long, 0.0001)

    # 11. 计算 divide(ts_delta(divide(ts_sum(multiply(close, vol), 20), ts_sum(vol, 20)), 5), add(ts_delta(divide(ts_sum(multiply(close, vol), 90), ts_sum(vol, 90)), 10), 0.0001))
    factor = divide(data_ts_delta_short, data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()