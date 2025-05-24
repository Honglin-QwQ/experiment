import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, divide, ts_decay_exp_window, ts_delta, multiply

def factor_6060(data, **kwargs):
    """
    因子名称: VolWeightedPriceChangeDecayRanked_78997
    数学表达式: rank(divide(ts_decay_exp_window(multiply(ts_delta(close, 1), vol), d=15, factor=0.8), ts_decay_exp_window(vol, d=15, factor=0.8)))
    中文描述: 该因子计算过去15天内，每日收盘价变化与当日交易量的乘积的指数衰减加权平均值，再除以过去15天的交易量的指数衰减加权平均值，最后对结果进行横截面排名。相较于前一个因子，该因子将时间窗口调整到15天，衰减因子调整为0.8，并引入了rank操作符，将因子值转换为相对排名，以提高因子的稳健性和可比性。较高的因子排名可能表明近期价格上涨伴随着较高的交易量且近期趋势更强，而较低的因子排名可能表明价格下跌伴随着较高的交易量或价格变动不大，且近期趋势更弱。这有助于识别交易量对价格变动的短期影响及其持续性，并通过排名消除量纲影响。
    因子应用场景：
    1. 趋势识别：通过量价关系识别趋势的强弱。
    2. 市场情绪：量价齐升可能反映市场乐观情绪，反之则可能反映悲观情绪。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], d=1)
    # 2. 计算 multiply(ts_delta(close, 1), vol)
    data_multiply = multiply(data_ts_delta_close, data['vol'])
    # 3. 计算 ts_decay_exp_window(multiply(ts_delta(close, 1), vol), d=15, factor=0.8)
    data_ts_decay_exp_window_1 = ts_decay_exp_window(data_multiply, d=15, factor=0.8)
    # 4. 计算 ts_decay_exp_window(vol, d=15, factor=0.8)
    data_ts_decay_exp_window_2 = ts_decay_exp_window(data['vol'], d=15, factor=0.8)
    # 5. 计算 divide(ts_decay_exp_window(multiply(ts_delta(close, 1), vol), d=15, factor=0.8), ts_decay_exp_window(vol, d=15, factor=0.8))
    data_divide = divide(data_ts_decay_exp_window_1, data_ts_decay_exp_window_2)
    # 6. 计算 rank(divide(ts_decay_exp_window(multiply(ts_delta(close, 1), vol), d=15, factor=0.8), ts_decay_exp_window(vol, d=15, factor=0.8)))
    factor = rank(data_divide, rate = 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()