import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, ts_corr, sign, ts_delta

def factor_5879(data, **kwargs):
    """
    因子名称: Volumetric_Price_Trend_Consistency_69892
    数学表达式: ts_decay_exp_window(ts_corr(sign(ts_delta(close, 1)), sign(ts_delta(vol, 1)), 10), d=20, factor=0.7)
    中文描述: 该因子旨在衡量近期价格变化方向与成交量变化方向的一致性，并对这种一致性应用指数衰减加权平均。具体来说，它首先计算过去10天收盘价日变化方向（上涨为1，下跌为-1，不变为0）与成交量日变化方向之间的滚动相关性，然后对该相关性序列应用指数衰减加权平均，衰减窗口为20天，衰减因子为0.7。相较于参考因子，创新点在于直接关注价格和成交量的'方向'一致性，使用`sign`操作符过滤掉具体的数值大小，从而降低噪音并突出趋势的同步性。同时，调整了相关性计算的时间窗口和指数衰减的参数。高因子值可能表明价格和成交量变化方向高度一致，预示当前趋势的持续性较强；低因子值可能表明价格和成交量变化方向不一致，预示趋势可能面临反转或缺乏支撑。该因子可以用于识别量价配合良好的趋势，并根据方向一致性判断趋势的强度和可持续性。
    因子应用场景：
    1. 趋势识别：识别量价配合良好的趋势，判断趋势的强度和可持续性。
    2. 反转预警：价格和成交量变化方向不一致时，预示趋势可能面临反转。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 2. 计算 sign(ts_delta(close, 1))
    data_sign_ts_delta_close = sign(data_ts_delta_close)
    # 3. 计算 ts_delta(vol, 1)
    data_ts_delta_vol = ts_delta(data['vol'], 1)
    # 4. 计算 sign(ts_delta(vol, 1))
    data_sign_ts_delta_vol = sign(data_ts_delta_vol)
    # 5. 计算 ts_corr(sign(ts_delta(close, 1)), sign(ts_delta(vol, 1)), 10)
    data_ts_corr = ts_corr(data_sign_ts_delta_close, data_sign_ts_delta_vol, 10)
    # 6. 计算 ts_decay_exp_window(ts_corr(sign(ts_delta(close, 1)), sign(ts_delta(vol, 1)), 10), d=20, factor=0.7)
    factor = ts_decay_exp_window(data_ts_corr, d=20, factor=0.7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()