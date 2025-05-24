import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5768(data, **kwargs):
    """
    因子名称: Volatility_Adjusted_Volume_Fraction_84467
    数学表达式: divide(fraction(ts_std_dev(vol, 10)), ts_mean(adv(vol, 20), 50))
    中文描述: 该因子结合了参考因子中的波动性概念和分数部分提取，并引入了成交量数据。首先计算过去10天成交量的标准差，提取其小数部分，以捕捉短期成交量波动的精细特征。然后将其除以过去50天20日平均成交量的均值，对短期波动进行长期成交量水平的标准化。这旨在识别短期成交量波动相对于长期平均活跃度的异常情况，可能预示着市场情绪的变化或资金流动的异常。创新点在于将成交量的波动性与分数部分提取结合，并进行长期平均成交量的标准化，提供了一个新的视角来衡量市场活跃度的微观结构变化。
    因子应用场景：
    1. 识别短期成交量波动相对于长期平均活跃度的异常情况。
    2. 预测市场情绪的变化或资金流动的异常。
    """
    # 1. 计算 ts_std_dev(vol, 10)
    data_ts_std_dev = ts_std_dev(data['vol'], 10)
    # 2. 计算 fraction(ts_std_dev(vol, 10))
    data_fraction = fraction(data_ts_std_dev)
    # 3. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], 20)
    # 4. 计算 ts_mean(adv(vol, 20), 50)
    data_ts_mean = ts_mean(data_adv, 50)
    # 5. 计算 divide(fraction(ts_std_dev(vol, 10)), ts_mean(adv(vol, 20), 50))
    factor = divide(data_fraction, data_ts_mean)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()