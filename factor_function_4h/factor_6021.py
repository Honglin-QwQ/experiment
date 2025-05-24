import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_delta, ts_decay_linear

def factor_6021(data, **kwargs):
    """
    因子名称: VWAP_Volume_Weighted_Price_Change_Correlation_51447
    数学表达式: ts_corr(ts_delta(close, 1), ts_decay_linear(vol, 10), 15)
    中文描述: 该因子计算每日收盘价变化与过去10天成交量线性衰减加权平均值在过去15天内的相关性。它旨在捕捉价格变动与近期成交量活跃度之间的关系。当价格上涨伴随近期成交量的线性衰减加权平均值增加时，相关性趋于正；当价格下跌伴随近期成交量的线性衰减加权平均值减少时，相关性也趋于正。正的相关性可能预示着价格趋势得到了近期成交量的支持，具有持续性。相较于参考因子，该因子引入了收盘价变化作为价格动量的衡量，并使用线性衰减加权平均成交量，更能反映近期成交量对价格的影响，同时通过相关性避免了硬性的阈值判断，保留了更多信息。改进建议中提到的使用更平滑的函数和引入动量因子的思想在该因子中得到了体现，通过计算收盘价delta和成交量衰减加权平均后的相关性，实现了动量和近期活跃度之间的平滑关联。
    因子应用场景：
    1. 趋势判断：用于判断价格趋势是否得到成交量的支持。
    2. 市场活跃度分析：通过成交量的线性衰减加权平均，更侧重近期成交量对价格的影响。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], d=1)

    # 2. 计算 ts_decay_linear(vol, 10)
    data_ts_decay_linear_vol = ts_decay_linear(data['vol'], d=10)

    # 3. 计算 ts_corr(ts_delta(close, 1), ts_decay_linear(vol, 10), 15)
    factor = ts_corr(data_ts_delta_close, data_ts_decay_linear_vol, d=15)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()