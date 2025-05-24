import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5890(data, **kwargs):
    """
    数学表达式: ts_rank(ts_decay_linear(ts_corr(ts_delta(close, 1), vol, 10), 20), 60)
    中文描述: 该因子计算过去10天每日收盘价变化与成交量之间的相关性，并对该相关性进行20天的线性衰减加权，时间越近的权重越高。最后，对衰减加权后的相关性在过去60天内进行排名。该因子旨在捕捉成交量与价格变动同步性的持续性，并结合历史排名进行评估。相较于参考因子，该因子创新性地结合了价格变动、成交量、时间序列相关性、线性衰减和时间序列排名，更全面地衡量了价量关系的动态变化和持续性，具有更强的预测潜力。高排名可能表明近期成交量与价格同向变动的趋势持续加强，预示着潜在的趋势延续；低排名则可能表示这种同步性减弱，可能预示着趋势的反转。这可以用于识别潜在的趋势形成或反转信号，并结合历史排名提供更全面的分析视角。
    因子应用场景：
    1. 趋势识别：通过分析成交量与价格变动的相关性，辅助识别市场趋势。
    2. 反转信号：当同步性减弱时，可能预示趋势反转，提供交易信号。
    3. 量价关系分析：全面衡量价量关系的动态变化和持续性，辅助投资决策。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 2. 计算 ts_corr(ts_delta(close, 1), vol, 10)
    data_ts_corr = ts_corr(data_ts_delta_close, data['vol'], 10)
    # 3. 计算 ts_decay_linear(ts_corr(ts_delta(close, 1), vol, 10), 20)
    data_ts_decay_linear = ts_decay_linear(data_ts_corr, 20)
    # 4. 计算 ts_rank(ts_decay_linear(ts_corr(ts_delta(close, 1), vol, 10), 20), 60)
    factor = ts_rank(data_ts_decay_linear, 60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()