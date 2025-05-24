import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_6089(data, **kwargs):
    """
    因子名称: DecayedVolatilityVolumeRatio_v2_10053
    数学表达式: divide(ts_decay_linear(ts_std_dev(log(close), 5), 15), ts_decay_linear(ts_std_dev(log(vol), 5), 15))
    中文描述: 该因子是PriceVolumeDecayRatio因子的改进版本。它计算过去5天收盘价对数收益率标准差的15天线性衰减平均值与过去5天成交量对数标准差的15天线性衰减平均值之比。通过使用对数和标准差，因子能够更稳定地衡量价格和成交量的波动性，并使用线性衰减赋予近期数据更高的权重。较高的值可能表明价格波动在相对较低的成交量波动下发生，这可能预示着趋势的脆弱性或潜在的反转。相较于原始因子，该因子通过引入对数和标准差来增强对波动率信息的捕捉，并优化了时间衰减参数的窗口期，旨在提高因子的预测能力和稳定性。
    因子应用场景：
    1. 趋势反转识别：较高的因子值可能预示着趋势的脆弱性或潜在的反转。
    2. 波动性分析：衡量价格和成交量的波动性，帮助识别市场风险。
    """
    # 1. 计算 log(close)
    data['log_close'] = log(data['close'])
    # 2. 计算 ts_std_dev(log(close), 5)
    data['std_dev_log_close'] = ts_std_dev(data['log_close'], 5)
    # 3. 计算 ts_decay_linear(ts_std_dev(log(close), 5), 15)
    data['decay_std_dev_log_close'] = ts_decay_linear(data['std_dev_log_close'], 15)
    # 4. 计算 log(vol)
    data['log_vol'] = log(data['vol'])
    # 5. 计算 ts_std_dev(log(vol), 5)
    data['std_dev_log_vol'] = ts_std_dev(data['log_vol'], 5)
    # 6. 计算 ts_decay_linear(ts_std_dev(log(vol), 5), 15)
    data['decay_std_dev_log_vol'] = ts_decay_linear(data['std_dev_log_vol'], 15)
    # 7. 计算 divide(ts_decay_linear(ts_std_dev(log(close), 5), 15), ts_decay_linear(ts_std_dev(log(vol), 5), 15))
    factor = divide(data['decay_std_dev_log_close'], data['decay_std_dev_log_vol'])

    # 删除中间变量
    del data['log_close']
    del data['std_dev_log_close']
    del data['decay_std_dev_log_close']
    del data['log_vol']
    del data['std_dev_log_vol']
    del data['decay_std_dev_log_vol']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()