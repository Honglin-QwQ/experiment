import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, multiply, ts_delta

def factor_5968(data, **kwargs):
    """
    因子名称: WeightedPriceDeltaVolatilityRatio_Enhanced_35107
    数学表达式: divide(ts_std_dev(multiply(close, ts_delta(vol, 1)), 15), ts_std_dev(multiply(ts_delta(close, 1), ts_delta(vol, 1)), 15))
    中文描述: 该因子计算过去15天内收盘价乘以日成交量变化的标准差与过去15天内日收盘价变化乘以日成交量变化的标准差之比。相较于参考因子，创新点在于使用日成交量变化（ts_delta(vol, 1)）作为加权因子，而非原始成交量。这使得因子更侧重于捕捉成交量变动对价格波动的影响，而非绝对成交量水平的影响。分子反映了成交量变动对收盘价绝对水平波动的影响，分母反映了成交量变动对日价格变动波动的影响。高因子值可能表明成交量变动更多地影响价格水平的波动而非日内变动，或者日内变动在成交量变动加权下相对稳定。这可能用于识别在成交量变动驱动下价格波动模式的变化，潜在地捕捉趋势的稳定或反转信号。结合了成交量变动对价格水平和价格变化的双重加权，并计算其波动性比率，提供了对市场动能和波动结构的新视角，特别关注了成交量变化的驱动作用。根据历史评估结果，该因子将时间窗口调整为15天，以尝试优化参数，提高预测能力。同时，通过引入成交量变化作为加权因子，旨在增强因子对市场情绪和交易活跃度变化的敏感性，从而提升统计显著性和稳定性。
    因子应用场景：
    1. 市场情绪分析：用于衡量成交量变化对价格波动的影响，辅助判断市场情绪。
    2. 趋势识别：识别成交量变动驱动下的价格波动模式，捕捉趋势的稳定或反转信号。
    3. 波动性结构分析：提供对市场动能和波动结构的新视角，特别关注成交量变化的驱动作用。
    """
    # 1. 计算 ts_delta(vol, 1)
    data_ts_delta_vol = ts_delta(data['vol'], d = 1)
    # 2. 计算 multiply(close, ts_delta(vol, 1))
    data_multiply_close_ts_delta_vol = multiply(data['close'], data_ts_delta_vol)
    # 3. 计算 ts_std_dev(multiply(close, ts_delta(vol, 1)), 15)
    data_ts_std_dev_numerator = ts_std_dev(data_multiply_close_ts_delta_vol, d = 15)
    # 4. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], d = 1)
    # 5. 计算 multiply(ts_delta(close, 1), ts_delta(vol, 1))
    data_multiply_ts_delta_close_ts_delta_vol = multiply(data_ts_delta_close, data_ts_delta_vol)
    # 6. 计算 ts_std_dev(multiply(ts_delta(close, 1), ts_delta(vol, 1)), 15)
    data_ts_std_dev_denominator = ts_std_dev(data_multiply_ts_delta_close_ts_delta_vol, d = 15)
    # 7. 计算 divide(ts_std_dev(multiply(close, ts_delta(vol, 1)), 15), ts_std_dev(multiply(ts_delta(close, 1), ts_delta(vol, 1)), 15))
    factor = divide(data_ts_std_dev_numerator, data_ts_std_dev_denominator)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()