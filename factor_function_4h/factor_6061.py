import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank
from operators import divide
from operators import ts_std_dev
from operators import ts_returns
from operators import s_log_1p
import pandas as pd

def factor_6061(data, **kwargs):
    """
    数学表达式: rank(divide(ts_std_dev(ts_returns(close, 3), 15), s_log_1p(vol)))
    中文描述: 该因子旨在捕捉短期价格波动率与平滑交易量比率的横截面排名。它首先计算过去15天内收盘价3日收益率的标准差，作为短期市场波动性的度量。接着，使用s_log_1p运算符对当前交易量进行平滑处理，以减轻极端交易量的影响并保留其相对变化信息。然后，将短期波动率除以平滑后的交易量，得到波动率与交易量的比率。最后，计算该比率在横截面上的排名。与历史输出的因子相比，该因子采用了比率而非乘法，并进一步对结果进行了排名，这可能更好地捕捉相对强度，并减轻极端比率值的影响。高排名可能表示在相对较低的交易量下出现了较高的波动，这可能预示着市场情绪的脆弱或潜在的价格反转。
    因子应用场景：
    1. 市场情绪分析：用于识别在交易量相对较低的情况下出现较高价格波动的股票，可能反映市场参与者的不确定性或情绪波动。
    2. 潜在反转信号：高排名可能预示着市场情绪的脆弱或潜在的价格反转，可以作为交易决策的参考信号。
    """
    # 1. 计算 ts_returns(close, 3)
    data_ts_returns = ts_returns(data['close'], 3)
    # 2. 计算 ts_std_dev(ts_returns(close, 3), 15)
    data_ts_std_dev = ts_std_dev(data_ts_returns, 15)
    # 3. 计算 s_log_1p(vol)
    data_s_log_1p = s_log_1p(data['vol'])
    # 4. 计算 divide(ts_std_dev(ts_returns(close, 3), 15), s_log_1p(vol))
    data_divide = divide(data_ts_std_dev, data_s_log_1p)
    # 5. 计算 rank(divide(ts_std_dev(ts_returns(close, 3), 15), s_log_1p(vol)))
    factor = rank(data_divide, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()