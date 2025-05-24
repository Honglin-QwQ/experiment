import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_mean, divide, ts_corr, jump_decay

def factor_6047(data, **kwargs):
    """
    数学表达式: jump_decay(ts_corr(divide(ts_std_dev(close, 10), ts_mean(close, 10)), vol, 5), d = 7, sensitivity = 0.025, force = 0.3)
    中文描述: 该因子在参考因子的基础上进行了创新，不再仅仅计算价格波动率的跳跃衰减，而是计算价格波动率（收盘价在过去10天内的标准差与均值之比）与成交量在过去5天内的相关性，然后对这个相关性序列应用跳跃衰减函数jump_decay。jump_decay会检测波动率与成交量相关性序列中的显著跳跃，并计算一个衰减贡献值。具体来说，它比较当前相关性与过去7天内的相关性，如果存在显著的跳跃（由sensitivity参数控制），则计算一个衰减值（由force参数控制）。这个因子旨在捕捉价格波动率与成交量之间关系的突发变化，并对其进行平滑处理。高因子值可能表示近期波动率与成交量之间的相关性出现了显著且相对持续的上升或下降（取决于相关性的正负），而低因子值可能表示相关性较低或跳跃不显著。这可以用于识别由成交量驱动的价格波动趋势的变化信号。
    因子应用场景：
    1. 波动率与成交量关系分析：用于识别价格波动率与成交量之间关系的突发变化。
    2. 趋势变化信号识别：识别由成交量驱动的价格波动趋势的变化信号。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], d = 10)
    # 2. 计算 ts_mean(close, 10)
    data_ts_mean = ts_mean(data['close'], d = 10)
    # 3. 计算 divide(ts_std_dev(close, 10), ts_mean(close, 10))
    data_divide = divide(data_ts_std_dev, data_ts_mean)
    # 4. 计算 ts_corr(divide(ts_std_dev(close, 10), ts_mean(close, 10)), vol, 5)
    data_ts_corr = ts_corr(data_divide, data['vol'], d = 5)
    # 5. 计算 jump_decay(ts_corr(divide(ts_std_dev(close, 10), ts_mean(close, 10)), vol, 5), d = 7, sensitivity = 0.025, force = 0.3)
    factor = jump_decay(data_ts_corr, d = 7, sensitivity = 0.025, force = 0.3)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()