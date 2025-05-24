import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_decay_linear, multiply, ts_std_dev, divide
import pandas as pd

def factor_6036(data, **kwargs):
    """
    因子名称: Volume_Weighted_Price_Volatility_Ratio_80492
    数学表达式: divide(ts_decay_linear(multiply(vol, close), 10), ts_std_dev(close, 20))
    中文描述: 该因子旨在衡量成交量加权价格的线性衰减平均值与收盘价波动率之间的比率。首先，计算每日成交量与收盘价的乘积，并对该乘积在过去10天内进行线性衰减平均。这部分捕捉了近期成交量活跃度与价格水平的综合信息，并给予近期数据更高的权重。同时，计算过去20天收盘价的标准差，衡量价格的波动性。最后，将成交量加权价格的线性衰减平均值除以收盘价的标准差。较高的因子值可能表明近期成交量活跃且价格水平较高，同时价格波动性相对较低，可能预示着市场处于稳步上涨或吸筹阶段；较低的因子值可能表明近期成交量不活跃或价格水平较低，同时价格波动性相对较高，可能预示着市场处于下跌或震荡阶段。相较于参考因子，该因子创新性地使用了成交量与价格的乘积作为基础，并结合了线性衰减平均和标准差，通过比率的形式更全面地捕捉量价关系和波动性特征，具有一定的创新性，可以用于识别不同市场阶段的特征。
    因子应用场景：
    1. 市场阶段识别：用于识别市场是处于稳步上涨、吸筹阶段还是下跌、震荡阶段。
    2. 量价关系分析：帮助分析成交量与价格之间的关系，判断量价是否配合。
    3. 波动性评估：结合价格波动率，评估市场的稳定性和风险。
    """
    # 1. 计算 multiply(vol, close)
    data_multiply = multiply(data['vol'], data['close'])
    # 2. 计算 ts_decay_linear(multiply(vol, close), 10)
    data_ts_decay_linear = ts_decay_linear(data_multiply, d = 10)
    # 3. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], d = 20)
    # 4. 计算 divide(ts_decay_linear(multiply(vol, close), 10), ts_std_dev(close, 20))
    factor = divide(data_ts_decay_linear, data_ts_std_dev)

    # 删除中间变量
    del data_multiply
    del data_ts_decay_linear
    del data_ts_std_dev

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()