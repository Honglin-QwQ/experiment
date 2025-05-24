import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, rank, ts_decay_linear, ts_returns, ts_std_dev
import pandas as pd

def factor_5776(data, **kwargs):
    """
    因子名称: Volatility_Adjusted_Decay_Rank_Difference_91904
    数学表达式: subtract(rank(ts_decay_linear(ts_returns(close, 3), 5, dense=False)), rank(ts_std_dev(ts_returns(close, 3), 5)))
    中文描述: 该因子旨在通过比较短期衰减收益率的排名与短期收益率波动率的排名来捕捉市场情绪和风险调整后的动量。首先计算过去3天的收盘价收益率，并在过去5天内对这些收益率应用线性衰减加权平均，赋予近期收益率更高的权重。同时，计算过去5天收益率的标准差。然后，分别计算衰减收益率和标准差在截面上的排名（0到1之间）。最后，用衰减收益率的排名减去标准差的排名。

    创新点：
    1. 结合了时间序列衰减（ts_decay_linear）和截面排名（rank），同时考虑了时间维度上的动量和截面维度上的相对表现。
    2. 通过比较衰减收益率排名和波动率排名的差异，提供了一种风险调整后动量的视角，关注那些在近期表现出较强且相对低波动动量的股票。
    3. 使用减法操作符（subtract）直接比较两个排名的相对位置，而非简单的除法，可以更清晰地看到衰减动量相对于波动性的强弱关系。

    应用场景：
    该因子可用于识别那些在近期表现出强劲衰减动量，且其波动性相对于其他股票较低的标的。这可能适用于风险厌恶型投资者或寻求稳定动量信号的策略。
    """
    # 1. 计算 ts_returns(close, 3)
    data_ts_returns = ts_returns(data['close'], 3)
    # 2. 计算 ts_decay_linear(ts_returns(close, 3), 5, dense=False)
    data_ts_decay_linear = ts_decay_linear(data_ts_returns, 5, dense=False)
    # 3. 计算 rank(ts_decay_linear(ts_returns(close, 3), 5, dense=False))
    data_rank_decay = rank(data_ts_decay_linear, 2)
    # 4. 计算 ts_std_dev(ts_returns(close, 3), 5)
    data_ts_std_dev = ts_std_dev(data_ts_returns, 5)
    # 5. 计算 rank(ts_std_dev(ts_returns(close, 3), 5))
    data_rank_std = rank(data_ts_std_dev, 2)
    # 6. 计算 subtract(rank(ts_decay_linear(ts_returns(close, 3), 5, dense=False)), rank(ts_std_dev(ts_returns(close, 3), 5)))
    factor = subtract(data_rank_decay, data_rank_std, filter = False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()