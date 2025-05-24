import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, ts_std_dev, rank, ts_corr, ts_delta, add, multiply

def factor_5783(data, **kwargs):
    """
    因子名称: Volatility_Decay_Momentum_Correlation_55092
    数学表达式: add(ts_decay_linear(ts_std_dev(close, 20), 10), multiply(rank(ts_corr(vol, low, 15)), ts_delta(close, 5)))
    中文描述: 该因子结合了波动率衰减、成交量与最低价的相关性排名以及短期价格动量。首先计算过去20天收盘价标准差的10天线性衰减加权平均值，捕捉近期波动率的变化趋势。
            然后计算过去15天成交量与最低价相关性的排名，反映价量关系的相对强弱。最后计算过去5天收盘价的差分，衡量短期价格动量。
            将波动率衰减值与相关性排名和短期价格动量的乘积相加，形成一个综合因子。
            创新点在于结合了不同时间窗口和不同类型的市场信息，通过线性衰减和排名操作引入非线性特征，
            旨在捕捉市场在波动率、价量关系和短期动量之间的复杂相互作用，可用于识别潜在的反转或趋势延续信号。
    因子应用场景：
    1. 波动率分析：通过波动率衰减，可以识别波动率变化的趋势，用于判断市场风险水平。
    2. 价量关系：成交量与最低价的相关性排名可以反映市场买卖力量的对比，辅助判断趋势的可靠性。
    3. 短期动量：短期价格动量可以捕捉市场短期内的价格变化，用于短线交易。
    """
    # 1. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 2. 计算 ts_decay_linear(ts_std_dev(close, 20), 10)
    data_ts_decay_linear = ts_decay_linear(data_ts_std_dev, 10)
    # 3. 计算 ts_corr(vol, low, 15)
    data_ts_corr = ts_corr(data['vol'], data['low'], 15)
    # 4. 计算 rank(ts_corr(vol, low, 15))
    data_rank = rank(data_ts_corr, 2)
    # 5. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 6. 计算 multiply(rank(ts_corr(vol, low, 15)), ts_delta(close, 5))
    data_multiply = multiply(data_rank, data_ts_delta)
    # 7. 计算 add(ts_decay_linear(ts_std_dev(close, 20), 10), multiply(rank(ts_corr(vol, low, 15)), ts_delta(close, 5)))
    factor = add(data_ts_decay_linear, data_multiply)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()