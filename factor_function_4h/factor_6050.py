import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_decay_exp_window, ts_delta, ts_corr, ts_returns

def factor_6050(data, **kwargs):
    """
    因子名称: Volume_Price_Momentum_Decay_Skew_58494
    数学表达式: ts_skewness(ts_decay_exp_window(ts_delta(volume, 3), d=10, factor=0.7), 20) * ts_corr(ts_returns(close, d=5), ts_delta(amount, 2), 15)
    中文描述: 该因子旨在捕捉成交量变化、价格动量、交易额变化以及这些指标的偏度与相关性之间的复杂动态。首先，计算过去3天成交量变化的10天指数衰减加权平均值的20天滚动偏度，这部分衡量了近期成交量变化趋势的非对称性，并引入了指数衰减的平滑和权重分配。然后，将这个偏度值乘以过去5天收盘价收益率与过去2天交易额变化之间的15天滚动相关性，这结合了短期价格动量与资金流动的关系。该因子的创新点在于：1. 引入了指数衰减加权平均（ts_decay_exp_window），使得近期成交量变化对偏度的影响更大，捕捉更及时的市场情绪；2. 结合了价格收益率（ts_returns）和交易额变化（ts_delta），从量价两个维度捕捉动量和资金流向，并使用相关性衡量其配合程度；3. 结构上通过乘法组合偏度与相关性，试图发现非线性的市场模式。相较于参考因子，该因子在成交量变化的处理上使用了指数衰减，引入了价格收益率作为价格动量指标，并简化了结构，移除了主动买入量排名部分，更专注于量价动量和偏度特征。当因子值为正时，可能表明近期成交量变化趋势具有正偏度（即有更多较大的正向变化），同时价格动量与资金流动呈正相关，可能预示着价格上涨动量；当因子值为负时，可能预示着相反的市场状态，可能预示着价格下跌动量。
    因子应用场景：
    1. 市场情绪捕捉：通过成交量变化的偏度来反映市场参与者的情绪，正偏度可能意味着乐观情绪，反之则为悲观情绪。
    2. 量价关系验证：结合价格收益率和交易额变化的相关性，验证量价配合的有效性，辅助判断趋势的可持续性。
    3. 趋势反转识别：当成交量偏度与量价相关性出现背离时，可能预示着趋势的反转。
    """
    # 1. 计算 ts_delta(volume, 3)
    data_ts_delta_volume = ts_delta(data['vol'], d=3)
    # 2. 计算 ts_decay_exp_window(ts_delta(volume, 3), d=10, factor=0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_delta_volume, d=10, factor=0.7)
    # 3. 计算 ts_skewness(ts_decay_exp_window(ts_delta(volume, 3), d=10, factor=0.7), 20)
    data_ts_skewness = ts_skewness(data_ts_decay_exp_window, d=20)
    # 4. 计算 ts_returns(close, d=5)
    data_ts_returns_close = ts_returns(data['close'], d=5)
    # 5. 计算 ts_delta(amount, 2)
    data_ts_delta_amount = ts_delta(data['amount'], d=2)
    # 6. 计算 ts_corr(ts_returns(close, d=5), ts_delta(amount, 2), 15)
    data_ts_corr = ts_corr(data_ts_returns_close, data_ts_delta_amount, d=15)
    # 7. 计算 ts_skewness(ts_decay_exp_window(ts_delta(volume, 3), d=10, factor=0.7), 20) * ts_corr(ts_returns(close, d=5), ts_delta(amount, 2), 15)
    factor = data_ts_skewness * data_ts_corr

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()