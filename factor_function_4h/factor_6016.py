import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_std_dev, ts_decay_linear, log
import pandas as pd
import numpy as np

def factor_6016(data, **kwargs):
    """
    因子名称: Volatility_Volume_Correlation_Decay_10140
    数学表达式: ts_corr(ts_std_dev(log(close), 15), ts_decay_linear(volume, 20), 10)
    中文描述: 该因子旨在捕捉短期价格波动率与近期成交量衰减之间的相关性。首先，计算过去15天收盘价对数收益率的标准差，作为短期价格波动率的度量。然后，计算过去20天成交量的线性衰减值，赋予近期成交量更高的权重。最后，计算这两者在过去10天内的滚动相关性。高因子值可能表明价格波动率与近期成交量衰减呈现正相关，即波动率上升时成交量趋于衰减，反之亦然。这可能用于识别市场情绪的变化或趋势的持续性。相较于参考因子，创新点在于结合了价格波动率（而非直接价格偏度）与成交量衰减，并计算了它们之间的相关性，以捕捉更复杂的市场动态。同时，根据评估报告的建议，使用了对数收益率的标准差来衡量波动率，并尝试了不同的时间窗口参数组合，以期提升因子的预测能力和稳定性。
    因子应用场景：
    1. 市场情绪识别：通过捕捉价格波动率与成交量衰减之间的关系，识别市场情绪的变化。
    2. 趋势持续性分析：评估当前趋势的稳定性和持续性。
    """
    # 1. 计算 log(close)
    data['log_close'] = log(data['close'])
    # 2. 计算 ts_std_dev(log(close), 15)
    data['volatility'] = ts_std_dev(data['log_close'], d=15)
    # 3. 计算 ts_decay_linear(volume, 20)
    data['volume_decay'] = ts_decay_linear(data['vol'], d=20)
    # 4. 计算 ts_corr(ts_std_dev(log(close), 15), ts_decay_linear(volume, 20), 10)
    factor = ts_corr(data['volatility'], data['volume_decay'], d=10)
    
    del data['log_close']
    del data['volatility']
    del data['volume_decay']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()