import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log, rank, ts_std_dev, divide
import pandas as pd
import numpy as np

def factor_5997(data, **kwargs):
    """
    因子名称: LogCloseRank_RelativeVolatility_23268
    数学表达式: divide(rank(log(close)), ts_std_dev(returns, 20))
    中文描述: 该因子结合了收盘价的对数排名和收益率的波动率。分子是对收盘价取自然对数后进行横截面排名，旨在捕捉平滑后的价格趋势在所有股票中的相对位置，降低绝对价格的影响并增强横截面可比性。分母是过去20天收益率的标准差，用于衡量股票的波动性。通过将对数收盘价排名除以波动率，该因子旨在识别那些在相对价格趋势稳定（排名较高）但波动性较低的股票。相较于参考因子，该因子用排名替代了直接的对数收盘价，增加了横截面比较的意义；同时延长了波动率计算的时间窗口，提高了稳定性。这符合改进建议中引入排名操作符和优化时间窗口的方向，并利用了可用的rank和ts_std_dev操作符。
    因子应用场景：
    1. 识别价格趋势稳定且波动性较低的股票：该因子可以帮助识别那些价格趋势相对稳定（排名较高）但波动性较低的股票，这些股票可能具有较高的投资价值。
    2. 风险调整收益：通过将价格趋势排名除以波动率，该因子可以用于风险调整收益的分析，帮助投资者找到在承担较低风险的同时，具有较高价格趋势的股票。
    """
    # 1. 计算 log(close)
    data_log_close = log(data['close'])
    # 2. 计算 rank(log(close))
    data_rank_log_close = rank(data_log_close)
    # 3. 计算 ts_std_dev(returns, 20)
    data_ts_std_dev_returns = ts_std_dev(data['returns'], 20)
    # 4. 计算 divide(rank(log(close)), ts_std_dev(returns, 20))
    factor = divide(data_rank_log_close, data_ts_std_dev_returns)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()