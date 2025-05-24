import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delta, ts_std_dev, ts_zscore, ts_decay_exp_window
import pandas as pd

def factor_6068(data, **kwargs):
    """
    数学表达式: rank(ts_delta(ts_std_dev(vol, 240), 1)) + ts_decay_exp_window(ts_zscore(vol, 97), 10, 0.8)
    中文描述: 该因子结合了长期成交量标准差的变化率排名和短期成交量Z分数的指数衰减加权平均。第一部分计算了过去240天成交量标准差的日变化量，并对其进行截面排名。这旨在捕捉长期成交量波动性的短期趋势变化。第二部分计算了成交量在过去97天内的Z分数，并对过去10天的Z分数进行指数衰减加权平均，衰减因子为0.8。这旨在识别当前成交量相对于其自身历史分布的异常程度，并赋予近期异常值更高的权重。将这两部分相加，旨在构建一个同时考虑长期波动性变化和短期异常程度及其近期趋势的综合因子。相较于参考因子，创新点在于：1. 对长期成交量波动性进行了差分处理，关注其变化率而非绝对值或相关性。2. 对短期成交量Z分数使用了指数衰减加权平均，更强调近期异常值的影响，并引入了新的操作符`ts_decay_exp_window`。3. 结合了变化率排名和指数衰减平均，提供了更动态的交易量分析视角。
    因子应用场景：
    1. 波动性趋势跟踪：捕捉成交量波动性变化趋势，辅助判断市场活跃度和潜在风险。
    2. 异常成交量识别：识别成交量相对于历史水平的异常程度，辅助发现潜在的交易机会。
    3. 综合分析：结合波动性趋势和异常程度，提供更全面的交易量分析，辅助决策。
    """
    # 1. 计算 ts_std_dev(vol, 240)
    data_ts_std_dev = ts_std_dev(data['vol'], 240)
    # 2. 计算 ts_delta(ts_std_dev(vol, 240), 1)
    data_ts_delta = ts_delta(data_ts_std_dev, 1)
    # 3. 计算 rank(ts_delta(ts_std_dev(vol, 240), 1))
    factor1 = rank(data_ts_delta, 2)
    # 4. 计算 ts_zscore(vol, 97)
    data_ts_zscore = ts_zscore(data['vol'], 97)
    # 5. 计算 ts_decay_exp_window(ts_zscore(vol, 97), 10, 0.8)
    factor2 = ts_decay_exp_window(data_ts_zscore, 10, 0.8)
    # 6. 计算 rank(ts_delta(ts_std_dev(vol, 240), 1)) + ts_decay_exp_window(ts_zscore(vol, 97), 10, 0.8)
    factor = factor1 + factor2

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()