import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, divide, ts_weighted_decay, log, signed_power, ts_std_dev, ts_returns

import pandas as pd
import numpy as np

def factor_5612(data, **kwargs):
    """
    数学表达式: ts_delta(divide(high + low, 2) - ts_weighted_decay(close, k = 0.2), d = 3) * signed_power(log(vol), 0.5) / ts_std_dev(ts_returns(close, d = 5), d = 15)
    中文描述: 本因子是对参考因子'(high + low)/2 - close'的创新性改进。它首先计算每日最高价和最低价的均值，然后减去收盘价的加权衰减值（权重因子为0.2），再计算该差值的三日差分。此外，该因子还引入了成交量取对数后的平方根，以反映市场对价格变动的置信度，并除以过去15天，5日收益率的标准差，以衡量市场波动率。该因子的创新之处在于综合考虑了收盘价的加权衰减值，成交量和波动率，从而更全面地捕捉市场情绪和价格变化的强度。该因子旨在识别短期内市场预期与实际收盘价之间的差异变化，并根据市场活跃度和波动程度进行调整，从而辅助判断价格趋势的潜在反转。
    因子应用场景：
    1. 市场情绪捕捉： 通过成交量和价格波动率的结合，辅助判断市场情绪。
    2. 趋势反转识别： 识别短期内市场预期与实际收盘价之间的差异变化，辅助判断价格趋势的潜在反转。
    """
    # 1. 计算 (high + low) / 2
    data['high_low_mean'] = divide(data['high'] + data['low'], 2)
    
    # 2. 计算 ts_weighted_decay(close, k = 0.2)
    data['close_weighted_decay'] = ts_weighted_decay(data['close'], k = 0.2)
    
    # 3. 计算 (high + low) / 2 - ts_weighted_decay(close, k = 0.2)
    data['diff'] = data['high_low_mean'] - data['close_weighted_decay']
    
    # 4. 计算 ts_delta(diff, d = 3)
    data['delta'] = ts_delta(data['diff'], d = 3)
    
    # 5. 计算 log(vol)
    data['log_vol'] = log(data['vol'])
    
    # 6. 计算 signed_power(log(vol), 0.5)
    data['signed_power_log_vol'] = signed_power(data['log_vol'], 0.5)
    
    # 7. 计算 ts_returns(close, d = 5)
    data['returns_5d'] = ts_returns(data['close'], d = 5)
    
    # 8. 计算 ts_std_dev(ts_returns(close, d = 5), d = 15)
    data['std_dev_returns'] = ts_std_dev(data['returns_5d'], d = 15)
    
    # 9. 计算 ts_delta(divide(high + low, 2) - ts_weighted_decay(close, k = 0.2), d = 3) * signed_power(log(vol), 0.5) / ts_std_dev(ts_returns(close, d = 5), d = 15)
    factor = data['delta'] * data['signed_power_log_vol'] / data['std_dev_returns']

    # 删除中间变量
    del data['high_low_mean']
    del data['close_weighted_decay']
    del data['diff']
    del data['delta']
    del data['log_vol']
    del data['signed_power_log_vol']
    del data['returns_5d']
    del data['std_dev_returns']
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()