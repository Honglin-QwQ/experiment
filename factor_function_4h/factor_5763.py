import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, ts_returns, ts_std_dev, divide

def factor_5763(data, **kwargs):
    """
    因子名称: Volatility_Adjusted_Momentum_Decay_70409
    数学表达式: ts_decay_linear(ts_returns(close, 3), 5, dense=False) / (ts_std_dev(ts_returns(close, 3), 5) + 1e-6)
    中文描述: 该因子旨在衡量短期收益率的线性衰减动量，并根据其短期波动性进行调整。首先计算过去3天的收盘价收益率，然后在过去5天内对这些收益率应用线性衰减加权平均，赋予近期收益率更高的权重。最后，将衰减后的收益率除以过去5天收益率的标准差（为避免除以零，加上一个很小的常数）。

    创新点：
    1. 结合了短期收益率的动量（通过ts_returns和ts_decay_linear实现）和波动性（通过ts_std_dev实现），提供了对风险调整后动量的视角。
    2. 使用线性衰减（ts_decay_linear）而非简单的移动平均，更能捕捉近期价格变化的趋势。
    3. 通过除以标准差，对动量进行了波动性调整，使得因子更能反映单位风险下的动量强度。

    应用场景：
    该因子可用于识别那些在近期表现出强劲且相对稳定的动量的股票，可能适用于动量策略或风险管理。
    """
    # 1. 计算 ts_returns(close, 3)
    returns_3 = ts_returns(data['close'], d=3, mode = 1)
    # 2. 计算 ts_decay_linear(ts_returns(close, 3), 5, dense=False)
    decay_linear = ts_decay_linear(returns_3, d=5, dense=False)
    # 3. 计算 ts_std_dev(ts_returns(close, 3), 5)
    std_dev = ts_std_dev(returns_3, d=5)
    # 4. 计算 (ts_std_dev(ts_returns(close, 3), 5) + 1e-6)
    std_dev_adjusted = std_dev + 1e-6
    # 5. 计算 ts_decay_linear(ts_returns(close, 3), 5, dense=False) / (ts_std_dev(ts_returns(close, 3), 5) + 1e-6)
    factor = divide(decay_linear, std_dev_adjusted)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()