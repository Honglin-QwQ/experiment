import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, ts_entropy, divide

def factor_5764(data, **kwargs):
    """
    因子名称: Volatility_Momentum_Entropy_Ratio_61943
    数学表达式: divide(ts_std_dev(ts_delta(close, 5), 10), ts_entropy(vol, 10))
    中文描述: 该因子通过计算收盘价5日变化的标准差与成交量10日信息熵的比值来衡量市场波动性、动量和不确定性之间的关系。分子捕获了短期价格变化的波动性，反映了价格动量的强度和稳定性。分母则量化了成交量分布的混乱程度，代表了市场交易活动的不确定性。当比值较高时，可能表明在相对确定的交易活动下，价格波动性较大，存在较强的趋势信号；当比值较低时，可能意味着在不确定的交易活动下，价格波动性较小，市场可能处于盘整或缺乏明确方向。这个因子结合了价格和成交量的信息，试图捕捉隐藏在市场噪音下的潜在交易机会。创新点在于将价格变化的标准差与成交量的信息熵相结合，提供了一个新的视角来理解市场动态。
    因子应用场景：
    1. 趋势识别：比值较高时，可能表明在相对确定的交易活动下，价格波动性较大，存在较强的趋势信号。
    2. 市场不确定性评估：分母量化了成交量分布的混乱程度，代表了市场交易活动的不确定性。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 2. 计算 ts_std_dev(ts_delta(close, 5), 10)
    data_ts_std_dev = ts_std_dev(data_ts_delta_close, 10)
    # 3. 计算 ts_entropy(vol, 10)
    data_ts_entropy = ts_entropy(data['vol'], 10)
    # 4. 计算 divide(ts_std_dev(ts_delta(close, 5), 10), ts_entropy(vol, 10))
    factor = divide(data_ts_std_dev, data_ts_entropy)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()