import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_decay_linear, divide, ts_delta, ts_std_dev

def factor_5730(data, **kwargs):
    """
    因子名称: VWAP_Momentum_Decay_Skew_73637
    数学表达式: ts_skewness(ts_decay_linear(divide(ts_delta(vwap, 5), ts_std_dev(vwap, 15)), 30), 90)
    中文描述: 该因子旨在捕捉经过线性衰减加权处理的VWAP短期动量相对于其短期波动性的偏度。首先计算VWAP在5天内的变化量，并将其除以VWAP在15天内的标准差，得到一个波动性调整后的短期动量信号。然后，对这个信号应用30天的线性衰减加权。最后，计算这个衰减加权后的波动性调整动量信号在过去90天内的偏度。正偏度可能表明近期存在一些大的正向波动，而负偏度可能表明存在大的负向波动。这个因子结合了短期动量、短期波动性、线性衰减加权和长期偏度，试图识别那些在波动性调整后的动量分布上存在异常偏斜的股票。创新点在于引入了ts_decay_linear操作符对波动性调整后的动量进行加权，以赋予近期数据更大的权重，并根据历史评估结果，进一步调整了delta和std_dev的窗口期，并扩展了ts_skewness的窗口期，以期提升因子的预测能力和稳定性。
    因子应用场景：
    1. 识别具有异常偏斜的股票：该因子可以帮助识别那些在波动性调整后的动量分布上存在异常偏斜的股票，这些股票可能存在潜在的投资机会。
    2. 辅助量化交易：该因子可以作为量化交易策略的一部分，用于识别具有特定偏度特征的股票，并进行相应的交易操作。
    """
    # 1. 计算 ts_delta(vwap, 5)
    data_ts_delta_vwap = ts_delta(data['vwap'], 5)
    # 2. 计算 ts_std_dev(vwap, 15)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 15)
    # 3. 计算 divide(ts_delta(vwap, 5), ts_std_dev(vwap, 15))
    data_divide = divide(data_ts_delta_vwap, data_ts_std_dev_vwap)
    # 4. 计算 ts_decay_linear(divide(ts_delta(vwap, 5), ts_std_dev(vwap, 15)), 30)
    data_ts_decay_linear = ts_decay_linear(data_divide, 30)
    # 5. 计算 ts_skewness(ts_decay_linear(divide(ts_delta(vwap, 5), ts_std_dev(vwap, 15)), 30), 90)
    factor = ts_skewness(data_ts_decay_linear, 90)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()