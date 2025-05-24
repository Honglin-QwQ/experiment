import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, multiply, ts_arg_min, ts_sum

def factor_5887(data, **kwargs):
    """
    因子名称: Close_LowPosition_VolumeRatio_86464
    数学表达式: divide(multiply(close, ts_arg_min(low, 5)), ts_sum(vol, 10))
    中文描述: 该因子名为“收盘价低点位置成交量比率因子”。它结合了当前收盘价、过去5天最低价出现的位置以及过去10天的总成交量。具体计算逻辑为：首先找到过去5天内最低价出现的相对位置（ts_arg_min(low, 5)），然后将当前收盘价与这个位置索引相乘，最后将结果除以过去10天的总成交量。这个因子的创新点在于将价格信息（收盘价和最低价位置）与成交量信息相结合，试图捕捉在价格接近近期低点时，市场活跃度（成交量）对价格动能的影响。较低的因子值可能表明在价格处于相对低位时，成交量较大，这可能预示着潜在的支撑或反转。该因子可用于识别价格触底反弹或持续下跌的信号，适用于趋势跟踪和反转策略。
    因子应用场景：
    1. 趋势识别：识别价格触底反弹或持续下跌的信号。
    2. 反转策略：在价格处于相对低位时，成交量较大，可能预示着潜在的支撑或反转。
    """
    # 1. 计算 ts_arg_min(low, 5)
    data_ts_arg_min = ts_arg_min(data['low'], 5)
    # 2. 计算 multiply(close, ts_arg_min(low, 5))
    data_multiply = multiply(data['close'], data_ts_arg_min)
    # 3. 计算 ts_sum(vol, 10)
    data_ts_sum = ts_sum(data['vol'], 10)
    # 4. 计算 divide(multiply(close, ts_arg_min(low, 5)), ts_sum(vol, 10))
    factor = divide(data_multiply, data_ts_sum)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()