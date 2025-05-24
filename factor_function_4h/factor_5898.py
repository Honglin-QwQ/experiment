import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, divide, multiply, ts_arg_min, ts_delta, ts_decay_linear

def factor_5898(data, **kwargs):
    """
    数学表达式: scale(divide(multiply(ts_arg_min(low, 7), ts_delta(close, 3)), ts_decay_linear(vol, 15)))
    中文描述: 该因子名为“缩放的低点位置时间序列变化成交量比率因子”。它在参考因子的基础上进行了创新，结合了过去7天最低价出现的位置、当前收盘价与3天前收盘价的差值（反映短期价格动量）以及过去15天成交量的线性衰减加权总和。具体计算逻辑为：首先找到过去7天内最低价出现的相对位置（ts_arg_min(low, 7)），然后计算当前收盘价与3天前收盘价的差值（ts_delta(close, 3)），将两者相乘。接着计算过去15天成交量的线性衰减加权总和（ts_decay_linear(vol, 15)），赋予近期成交量更大的权重。最后，将前两者的乘积除以成交量的衰减加权总和，并对结果进行标准化（scale）。

    创新点：
    1. **结构创新：** 引入了短期价格动量（ts_delta(close, 3)）来增强因子的预测能力，同时使用线性衰减加权成交量（ts_decay_linear(vol, 15)）来更敏感地捕捉近期的市场活跃度。
    2. **参数优化：** 调整了最低价位置的窗口期至7天，并使用了15天的成交量衰减窗口，这些参数的选择是基于对市场动态的考量，旨在捕捉不同时间尺度的信息。
    3. **标准化处理：** 对最终结果进行标准化（scale），使得因子值在不同股票和不同时间点之间具有可比性，有助于后续的因子组合和风险控制。

    该因子试图捕捉在价格接近近期低点时，短期价格动量和近期成交量对未来价格走势的影响。较高的因子值可能表明在价格处于相对低位时，存在积极的短期价格动量和较高的近期成交量，这可能预示着潜在的上涨动能。该因子可用于识别价格触底反弹或动量持续的信号，适用于趋势跟踪和反转策略，同时通过标准化提高了因子的可用性。

    因子应用场景：
    1. 趋势识别：当因子值较高时，表明价格处于相对低位时，存在积极的短期价格动量和较高的近期成交量，可能预示着潜在的上涨动能。
    2. 反转策略：识别价格触底反弹信号。
    3. 动量策略：识别价格动量持续信号。
    """
    # 1. 计算 ts_arg_min(low, 7)
    data_ts_arg_min_low = ts_arg_min(data['low'], d=7)
    # 2. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], d=3)
    # 3. 计算 multiply(ts_arg_min(low, 7), ts_delta(close, 3))
    data_multiply = multiply(data_ts_arg_min_low, data_ts_delta_close)
    # 4. 计算 ts_decay_linear(vol, 15)
    data_ts_decay_linear_vol = ts_decay_linear(data['vol'], d=15)
    # 5. 计算 divide(multiply(ts_arg_min(low, 7), ts_delta(close, 3)), ts_decay_linear(vol, 15))
    data_divide = divide(data_multiply, data_ts_decay_linear_vol)
    # 6. 计算 scale(divide(multiply(ts_arg_min(low, 7), ts_delta(close, 3)), ts_decay_linear(vol, 15)))
    factor = scale(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()