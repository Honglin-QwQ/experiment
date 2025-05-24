import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5854(data, **kwargs):
    """
    数学表达式: ts_rank(divide(ts_std_dev(close, 20), adv(vol, 20)), 60)
    中文描述: 该因子计算过去20天收盘价标准差与过去20天平均成交量的比值的过去60天时间序列排名。收盘价标准差衡量价格波动性，平均成交量反映市场活跃度。该因子通过结合价格波动性和成交量，并对其比值进行长期排名，旨在捕捉市场情绪和波动性在历史上的相对位置。较高的因子值可能表明当前价格波动性相对于成交量处于历史高位，可能预示着潜在的市场转折点或异常波动。
    因子应用场景：
    1. 市场情绪分析：用于识别市场情绪高涨或低迷时期。
    2. 波动性预测：用于预测市场波动性可能发生的转折点。
    3. 交易信号生成：结合其他技术指标，生成买入或卖出信号。
    """
    # 1. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 2. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], 20)
    # 3. 计算 divide(ts_std_dev(close, 20), adv(vol, 20))
    data_divide = divide(data_ts_std_dev, data_adv)
    # 4. 计算 ts_rank(divide(ts_std_dev(close, 20), adv(vol, 20)), 60)
    factor = ts_rank(data_divide, 60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()