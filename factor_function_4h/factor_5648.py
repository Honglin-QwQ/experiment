import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5648(data, **kwargs):
    """
    因子名称: factor_0007_11283
    数学表达式: rank(winsorize(scale(ts_corr(close, vol, 10)))) * (log(ts_sum(amount, 10)) * (amount / ts_mean(amount, 20))) - ts_rank(ts_std_dev(high, 14), 20)
    中文描述: 该因子是对factor_0006的改进，旨在提高因子的预测能力和鲁棒性。核心思想是结合价格与成交量的相关性、交易额的相对变化以及最高价波动率的排名。
    首先，计算收盘价与成交量在过去10天的相关性，并进行标准化和winsorize处理，以降低噪音。然后，乘以过去10天交易额总和的对数与当前成交额相对于过去20天平均成交额的比值，反映成交额的相对变化。
    最后，减去最高价的标准差在过去20天的排名，捕捉价格波动较大的股票。
    创新点在于：1. 增强了相关性部分的稳健性，降低噪音干扰；2. 引入了成交额的相对变化，可能更能捕捉市场情绪的变化；3. 使用最高价的标准差代替最高价差的绝对值，更能反映价格的波动幅度。
    因子应用场景：
    1. 预测股票收益：该因子结合了价格、成交量和交易额的信息，可能对股票的未来收益具有一定的预测能力。
    2. 风险管理：通过捕捉价格波动较大的股票，有助于识别潜在的风险。
    3. 市场情绪分析：成交额的相对变化可能反映市场情绪，有助于把握市场脉搏。
    """
    # 1. 计算 ts_corr(close, vol, 10)
    data_ts_corr = ts_corr(data['close'], data['vol'], 10)
    # 2. 计算 scale(ts_corr(close, vol, 10))
    data_scale = scale(data_ts_corr)
    # 3. 计算 winsorize(scale(ts_corr(close, vol, 10)))
    data_winsorize = winsorize(data_scale)
    # 4. 计算 rank(winsorize(scale(ts_corr(close, vol, 10))))
    data_rank = rank(data_winsorize, 2)
    # 5. 计算 ts_sum(amount, 10)
    data_ts_sum = ts_sum(data['amount'], 10)
    # 6. 计算 log(ts_sum(amount, 10))
    data_log = log(data_ts_sum)
    # 7. 计算 ts_mean(amount, 20)
    data_ts_mean = ts_mean(data['amount'], 20)
    # 8. 计算 amount / ts_mean(amount, 20)
    data_divide = divide(data['amount'], data_ts_mean)
    # 9. 计算 (log(ts_sum(amount, 10)) * (amount / ts_mean(amount, 20)))
    data_multiply = multiply(data_log, data_divide)
    # 10. 计算 ts_std_dev(high, 14)
    data_ts_std_dev = ts_std_dev(data['high'], 14)
    # 11. 计算 ts_rank(ts_std_dev(high, 14), 20)
    data_ts_rank = ts_rank(data_ts_std_dev, 20)
    # 12. 计算 rank(winsorize(scale(ts_corr(close, vol, 10)))) * (log(ts_sum(amount, 10)) * (amount / ts_mean(amount, 20))) - ts_rank(ts_std_dev(high, 14), 20)
    factor = subtract(multiply(data_rank, data_multiply), data_ts_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()