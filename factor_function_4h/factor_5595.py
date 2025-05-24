import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_arg_min, rank, ts_corr, adv, ts_delta

def factor_5595(data, **kwargs):
    """
    因子名称: factor_0001_49822
    数学表达式: ts_arg_min(close,14) + rank(ts_corr(adv20, ts_delta(close, 5), 10))
    中文描述: 该因子结合了短期最低价位置和量价相关性。ts_arg_min(close,14)表示过去14天内收盘价最低点出现的位置，rank(ts_corr(adv20, ts_delta(close, 5), 10))表示过去10天平均成交量与5日收盘价变化的相关性的排名。该因子旨在捕捉短期价格动量与成交量之间的关系，创新点在于结合了绝对价格位置信息和相对的量价相关性排名，可能用于识别价格反转或趋势延续的早期信号。
    因子应用场景：
    1. 识别价格反转信号：当ts_arg_min较低且量价相关性排名较高时，可能预示着价格即将反转。
    2. 确认趋势延续：当ts_arg_min较高且量价相关性排名也较高时，可能确认当前趋势将继续。
    """
    # 计算 ts_arg_min(close, 14)
    data_ts_arg_min = ts_arg_min(data['close'], 14)
    # 计算 adv(close, 20)
    data_adv20 = adv(data['close'], 20)
    # 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 计算 ts_corr(adv20, ts_delta(close, 5), 10)
    data_ts_corr = ts_corr(data_adv20, data_ts_delta, 10)
    # 计算 rank(ts_corr(adv20, ts_delta(close, 5), 10))
    data_rank = rank(data_ts_corr, 2)
    # 计算 ts_arg_min(close,14) + rank(ts_corr(adv20, ts_delta(close, 5), 10))
    factor = data_ts_arg_min + data_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()