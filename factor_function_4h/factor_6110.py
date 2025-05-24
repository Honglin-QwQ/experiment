import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_decay_linear, ts_rank
import pandas as pd

def factor_6110(data, **kwargs):
    """
    因子名称: Vol_Price_Correlation_Decay_Rank_44314
    数学表达式: ts_rank(ts_decay_linear(ts_corr(vol, close, 20), 10), 60)
    中文描述: 该因子旨在捕捉交易量与收盘价之间短期相关性的衰减趋势，并对其进行长期时间序列排名。因子表达式为ts_rank(ts_decay_linear(ts_corr(vol, close, 20), 10), 60)。
            首先，计算过去20天交易量与收盘价的滚动相关性，反映短期价量关系。然后，对该相关性序列进行10天的线性衰减处理，赋予近期相关性更高的权重，捕捉相关性的衰减趋势。
            最后，计算衰减后的相关性序列在过去60天的时间序列排名。较高的因子值表明当前交易量与价格的短期相关性经过衰减后，在较长的时间窗口内处于较高的排名，
            可能预示着市场情绪的持续影响或资金流动的强化。该因子结合了滚动相关性、线性衰减和时间序列排名，相较于简单的价量相关性或交易量排名，
            提供了更精细的价量关系分析视角，具有结构和逻辑上的创新性，并引入了ts_decay_linear操作符来捕捉衰减趋势，响应了改进建议中关于使用时间序列操作符提升因子的方向。
    因子应用场景：
    1.  量价关系分析：用于识别量价关系的变化趋势，判断市场是健康上涨还是背离下跌。
    2.  趋势判断：因子值较高可能预示着市场情绪的持续影响或资金流动的强化，有助于判断趋势的持续性。
    3.  市场情绪监控：通过量价相关性的衰减和排名，可以辅助判断市场情绪的变化。
    """
    # 1. 计算 ts_corr(vol, close, 20)
    data_ts_corr = ts_corr(data['vol'], data['close'], 20)
    # 2. 计算 ts_decay_linear(ts_corr(vol, close, 20), 10)
    data_ts_decay_linear = ts_decay_linear(data_ts_corr, 10)
    # 3. 计算 ts_rank(ts_decay_linear(ts_corr(vol, close, 20), 10), 60)
    factor = ts_rank(data_ts_decay_linear, 60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()