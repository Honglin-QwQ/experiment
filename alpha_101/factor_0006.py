import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import adv, ts_rank, ts_delta, sign, multiply

def factor_0006(data, **kwargs):
    """
    数学表达式: ((adv20 < volume) ? ((-1 * ts_rank(abs(ts_delta(close, 7)), 60)) * sign(ts_delta(close, 7))) : (-1 * 1))
    中文描述: 如果过去20天平均成交额小于当前成交量，则计算过去60天收盘价7日变化量绝对值的排名，并乘以收盘价7日变化量的符号，否则赋值为-1。该因子可能捕捉成交量放大情况下，价格变化趋势的持续性，应用场景包括：1. 量价齐升选股策略：选择因子值为正且绝对值较大的股票，预期上涨；2. 趋势反转策略：当因子值为负时，可能预示超买，进行反向操作；3. 波动率预测：因子绝对值越大，可能预示未来波动率增大。
    """
    # 计算过去20天平均成交额
    adv20_data = adv(data['vol'], d = 20)

    # 计算收盘价7日变化量
    ts_delta_close_7 = ts_delta(data['close'], d = 7)

    # 计算收盘价7日变化量绝对值
    abs_ts_delta_close_7 = abs(ts_delta_close_7)

    # 计算过去60天收盘价7日变化量绝对值的排名
    ts_rank_abs_ts_delta_60 = ts_rank(abs_ts_delta_close_7, d = 60)

    # 计算收盘价7日变化量的符号
    sign_ts_delta_close_7 = sign(ts_delta_close_7)

    # 计算(-1 * ts_rank(abs(ts_delta(close, 7)), 60)) * sign(ts_delta(close, 7))
    factor_cal = multiply(multiply(-1, ts_rank_abs_ts_delta_60), sign_ts_delta_close_7)

    # 如果过去20天平均成交额小于当前成交量，则计算过去60天收盘价7日变化量绝对值的排名，并乘以收盘价7日变化量的符号，否则赋值为-1
    factor = factor_cal.where(adv20_data < data['vol'], -1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()