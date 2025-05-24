import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, rank, ts_corr, ts_delta, multiply
import pandas as pd

def factor_5779(data, **kwargs):
    """
    因子名称: Volume_Weighted_Volatility_Momentum_68763
    数学表达式: multiply(ts_std_dev(close, 10), rank(ts_corr(volume, ts_delta(close, 5), 15)))
    中文描述: 该因子结合了价格波动率和量价动量的相关性。首先计算过去10日收盘价的标准差，衡量近期价格波动性。然后计算过去15日成交量与过去5日收盘价变化量（动量）之间的相关性，并对其进行排名。最后将波动率与量价动量相关性的排名相乘。高因子值可能表示在较高波动率环境下，成交量与短期价格动量呈现较强的相关性，这可能预示着趋势的加强。相较于参考因子，该因子创新性地将波动率与量价动量相关性排名结合，并使用乘法操作符，试图捕捉波动率对量价关系的影响，而非简单地用波动率进行标准化。
    因子应用场景：
    1. 趋势判断：因子值高可能表示趋势加强。
    2. 波动率量价关系分析：用于研究波动率对量价关系的影响。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 2. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 3. 计算 ts_corr(volume, ts_delta(close, 5), 15)
    data_ts_corr = ts_corr(data['vol'], data_ts_delta, 15)
    # 4. 计算 rank(ts_corr(volume, ts_delta(close, 5), 15))
    data_rank = rank(data_ts_corr, 2)
    # 5. 计算 multiply(ts_std_dev(close, 10), rank(ts_corr(volume, ts_delta(close, 5), 15)))
    factor = multiply(data_ts_std_dev, data_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()