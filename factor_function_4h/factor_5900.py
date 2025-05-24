import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, rank, ts_corr
import pandas as pd

def factor_5900(data, **kwargs):
    """
    因子名称: TS_DecayExp_Corr_Vol_Amount_Rank_78435
    数学表达式: ts_decay_exp_window(rank(ts_corr(vol, amount, 5)), 10, factor=0.7)
    中文描述: 该因子首先计算成交量(vol)和交易额(amount)在过去5天内的滚动相关性的横截面排名。然后，对这个排名序列应用一个10天窗口期的指数衰减加权平均，衰减因子为0.7。这个因子旨在捕捉近期价量关系强弱的相对变化，并对更近期的变化赋予更高的权重。高因子值可能表明近期成交量和交易额的正相关性排名较高，意味着市场活跃度和资金流入的相对增强，可能预示着上涨动能；低因子值则可能表明相关性排名较低，市场活跃度相对减弱，可能预示着下跌风险。相较于参考因子，该因子创新性地结合了成交量和交易额的相关性，并引入了指数衰减加权平均来平滑和突出近期趋势，同时利用横截面排名来捕捉相对强弱。这符合改进建议中简化相关性计算（虽然这里用了相关性，但通过rank和指数衰减进行了处理）、优化参数选择（引入了衰减因子）以及使用适当操作符（rank, ts_decay_exp_window）的方向。
    因子应用场景：
    1. 动量捕捉：识别近期价量关系强劲的股票，可能预示着上涨动能。
    2. 市场活跃度评估：评估市场整体的活跃程度和资金流入情况。
    3. 风险预警：识别价量关系减弱的股票，可能预示着下跌风险。
    """
    # 1. 计算 ts_corr(vol, amount, 5)
    data_ts_corr = ts_corr(data['vol'], data['amount'], 5)
    # 2. 计算 rank(ts_corr(vol, amount, 5))
    data_rank = rank(data_ts_corr, 2)
    # 3. 计算 ts_decay_exp_window(rank(ts_corr(vol, amount, 5)), 10, factor=0.7)
    factor = ts_decay_exp_window(data_rank, 10, factor=0.7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()