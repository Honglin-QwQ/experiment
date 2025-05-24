import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_arg_max, add, divide
import pandas as pd

def factor_5815(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(vwap, 30), add(ts_arg_max(close, 60), 1))
    中文描述: 该因子结合了VWAP的波动性和收盘价最大值的相对位置。首先，计算过去30天VWAP的标准差，衡量VWAP的波动性。然后，计算过去60天收盘价最大值的相对索引（加上1避免除以零）。最后，将VWAP的波动性除以收盘价最大值的相对索引（加1），形成因子。该因子旨在捕捉VWAP波动性与近期价格高点位置之间的关系。较高的VWAP波动性和较小的ts_arg_max值（近期出现价格高点）可能预示着市场处于强势或潜在的顶部区域。创新点在于使用ts_arg_max来衡量近期价格高点的位置，并将其与VWAP波动性结合，形成一个反映市场强度和潜在风险的指标。相较于参考因子，本因子简化了表达式，替换了对噪音敏感的ts_entropy和对异常值敏感的ts_arg_min，转而使用ts_std_dev和ts_arg_max，并引入了比率形式，以更直观地反映两个组成部分之间的相对关系。
    因子应用场景：
    1. 波动性分析：用于识别VWAP波动性较高且近期价格出现高点的股票，可能预示着市场关注度较高。
    2. 趋势判断：结合VWAP波动性和价格高点位置，辅助判断市场趋势的强度和潜在风险。
    3. 风险管理：识别VWAP波动性较高，但价格高点出现较早的股票，可能存在一定的回调风险。
    """
    # 1. 计算 ts_std_dev(vwap, 30)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 30)
    # 2. 计算 ts_arg_max(close, 60)
    data_ts_arg_max_close = ts_arg_max(data['close'], 60)
    # 3. 计算 add(ts_arg_max(close, 60), 1)
    data_add = add(data_ts_arg_max_close, 1)
    # 4. 计算 divide(ts_std_dev(vwap, 30), add(ts_arg_max(close, 60), 1))
    factor = divide(data_ts_std_dev_vwap, data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()