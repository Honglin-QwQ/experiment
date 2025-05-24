import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log, divide, ts_delay, ts_rank, ts_delta, ts_theilsen, sigmoid, multiply, rank
import pandas as pd
import numpy as np

def factor_5646(data, **kwargs):
    """
    因子名称: factor_VolumePriceMomentum_v3_21826
    数学表达式: multiply(rank(ts_rank(close, 10)), rank(log(divide(amount, ts_delay(amount, 5)))), rank(ts_delta(close, 5)), sigmoid(ts_theilsen(close, vol, 5)))
    中文描述: 该因子是对原始VolumePriceMomentum因子的改进版本，旨在更有效地捕捉价格动量和成交额变化之间的关系。ts_rank(close,10)衡量了过去10天收盘价的排名，反映了中期价格趋势的强度。log(divide(amount, ts_delay(amount, 5)))计算了当前成交额与5天前成交额的比率的对数，反映了成交额的相对变化。ts_delta(close, 5)计算了过去5天收盘价变化的差值，用于衡量价格变化的强度和方向。sigmoid(ts_theilsen(close, vol, 5))计算了过去5天收盘价和成交量的Theil-Sen斜率的sigmoid函数值，用于衡量价格趋势的加速或减速。创新点在于引入了sigmoid函数对价格变化进行平滑和归一化，从而更好地捕捉价格趋势的加速或减速。同时，将ts_rank的时间窗口从7天调整为10天，以适应更长期的价格趋势。另外，使用rank操作符增强非线性关系, 并且加入了成交量和价格的斜率指标，使得因子能更好的捕捉价格和成交量的关系。
    因子应用场景：
    1. 动量捕捉：用于捕捉价格和成交量之间的动量关系，辅助判断趋势的加速或减速。
    2. 趋势识别：结合价格排名、成交额变化和价格变化，识别中长期价格趋势。
    3. 成交量验证：通过成交量变化验证价格趋势的可靠性。
    """

    # 1. 计算 ts_rank(close, 10)
    data_ts_rank_close_10 = ts_rank(data['close'], d=10)

    # 2. 计算 rank(ts_rank(close, 10))
    data_rank_ts_rank_close_10 = rank(data_ts_rank_close_10)

    # 3. 计算 ts_delay(amount, 5)
    data_ts_delay_amount_5 = ts_delay(data['amount'], d=5)

    # 4. 计算 divide(amount, ts_delay(amount, 5))
    data_divide_amount_ts_delay_amount_5 = divide(data['amount'], data_ts_delay_amount_5)

    # 5. 计算 log(divide(amount, ts_delay(amount, 5)))
    data_log_divide_amount_ts_delay_amount_5 = log(data_divide_amount_ts_delay_amount_5)

    # 6. 计算 rank(log(divide(amount, ts_delay(amount, 5))))
    data_rank_log_divide_amount_ts_delay_amount_5 = rank(data_log_divide_amount_ts_delay_amount_5)

    # 7. 计算 ts_delta(close, 5)
    data_ts_delta_close_5 = ts_delta(data['close'], d=5)

    # 8. 计算 rank(ts_delta(close, 5))
    data_rank_ts_delta_close_5 = rank(data_ts_delta_close_5)

    # 9. 计算 ts_theilsen(close, vol, 5)
    data_ts_theilsen_close_vol_5 = ts_theilsen(data['close'], data['vol'], d=5)

    # 10. 计算 sigmoid(ts_theilsen(close, vol, 5))
    data_sigmoid_ts_theilsen_close_vol_5 = sigmoid(data_ts_theilsen_close_vol_5)

    # 11. 计算 multiply(rank(ts_rank(close, 10)), rank(log(divide(amount, ts_delay(amount, 5)))), rank(ts_delta(close, 5)), sigmoid(ts_theilsen(close, vol, 5)))
    factor = multiply(data_rank_ts_rank_close_10, data_rank_log_divide_amount_ts_delay_amount_5, data_rank_ts_delta_close_5, data_sigmoid_ts_theilsen_close_vol_5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()