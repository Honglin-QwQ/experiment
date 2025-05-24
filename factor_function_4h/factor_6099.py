import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_returns, ts_delta, ts_corr, rank

def factor_6099(data, **kwargs):
    """
    数学表达式: rank(ts_corr(ts_returns(vol, 5), ts_delta(close, 3), 10))
    中文描述: 该因子首先计算过去5天成交量的收益率，以及过去3天收盘价的差值。然后计算这两者在过去10天内的相关性，并对相关性结果进行排名。这个因子捕捉了短期价格变动与成交量变化率之间的关系，并通过排名来衡量这种关系的相对强弱。高排名可能表示近期价格和成交量变化率之间存在较强的正相关或负相关，这可能预示着趋势的持续或反转。它结合了参考因子中对成交量和价格差值的处理，并通过计算它们之间的相关性并进行排名，增加了因子的创新性和复杂性。
    因子应用场景：
    1. 趋势识别：当因子值较高时，表明成交量的收益率和收盘价差值高度相关，可能意味着当前趋势较强且稳定。
    2. 市场同步性分析：因子有助于识别市场中成交量变化与价格变化同步性较高的股票，这些股票可能对市场整体趋势更为敏感。
    """
    # 1. 计算 ts_returns(vol, 5)
    data_ts_returns_vol = ts_returns(data['vol'], 5)
    # 2. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], 3)
    # 3. 计算 ts_corr(ts_returns(vol, 5), ts_delta(close, 3), 10)
    data_ts_corr = ts_corr(data_ts_returns_vol, data_ts_delta_close, 10)
    # 4. 计算 rank(ts_corr(ts_returns(vol, 5), ts_delta(close, 3), 10))
    factor = rank(data_ts_corr, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()