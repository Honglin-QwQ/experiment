import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, rank

def factor_6087(data, **kwargs):
    """
    因子名称: Ranked_VWAP_Close_Momentum_Decay_62706
    数学表达式: ts_decay_linear(rank(vwap - close), 10)
    中文描述: 该因子计算过去10天内，每日成交量加权平均价（VWAP）与收盘价（close）之差的截面排名的线性衰减加权平均值。VWAP与收盘价的差值反映了当日交易的平均成本与最终收盘价的偏离程度，其截面排名则衡量了这种偏离在不同股票间的相对位置。通过对这个排名序列应用线性衰减加权，赋予近期的数据更高的权重，旨在捕捉近期市场情绪和交易力量的动量效应。与原因子关注波动性不同，该因子创新性地结合了VWAP与收盘价的相对差异、截面排名以及时间序列的线性衰减加权平均，用于衡量近期市场情绪和交易力量的持续方向，可能适用于识别潜在的趋势延续信号。因子改进建议中提到可以改变因子形式和使用非线性操作符，这里的线性衰减可以看作是一种对时间序列的加权处理，与简单的标准差计算不同，更侧重于近期数据的贡献，从而引入了动量元素。
    因子应用场景：
    1. 趋势识别：捕捉近期市场情绪和交易力量的动量效应，识别潜在的趋势延续信号。
    2. 市场情绪分析：通过VWAP与收盘价的差异排名，衡量市场参与者的平均交易成本与收盘价的偏离程度，反映市场情绪。
    """
    # 1. 计算 vwap - close
    vwap_minus_close = data['vwap'] - data['close']
    # 2. 计算 rank(vwap - close)
    data_rank = rank(vwap_minus_close, 2)
    # 3. 计算 ts_decay_linear(rank(vwap - close), 10)
    factor = ts_decay_linear(data_rank, d = 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()