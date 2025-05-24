import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, ts_weighted_decay, ts_skewness, multiply

def factor_5924(data, **kwargs):
    """
    数学表达式: ts_rank(ts_delta(vwap, 10) * ts_weighted_decay(vol, 0.6) * ts_skewness(close, 30), 60)
    中文描述: 该因子在参考因子的基础上进行了创新，结合了VWAP的短期变化、成交量的加权衰减以及收盘价的短期偏度。具体来说，它首先计算VWAP在过去10天的变化量，然后将这个变化量与经过权重衰减处理的成交量以及过去30天收盘价的偏度相乘。最后，计算这个乘积在过去60天内的排名。相较于参考因子，创新点在于引入了`ts_skewness`操作符，捕捉了近期价格分布的偏度信息，这可能反映了市场情绪的非对称性。同时，调整了`ts_delta`、`ts_weighted_decay`和`ts_rank`的时间窗口，以期找到更优的参数组合。高排名可能表明价格的短期变化与活跃成交量以及正偏度（价格上涨时涨幅大于下跌时跌幅）之间的协同效应较强，可用于识别潜在的动量机会或市场情绪的积极变化。
    因子应用场景：
    1. 动量机会识别：高排名可能指示价格的短期变化与成交量和价格偏度之间的协同效应，从而识别潜在的动量机会。
    2. 市场情绪分析：通过结合价格偏度，该因子有助于捕捉市场情绪的非对称性，从而辅助判断市场情绪的积极或消极变化。
    """
    # 1. 计算 ts_delta(vwap, 10)
    data_ts_delta_vwap = ts_delta(data['vwap'], 10)
    # 2. 计算 ts_weighted_decay(vol, 0.6)
    data_ts_weighted_decay_vol = ts_weighted_decay(data['vol'], 0.6)
    # 3. 计算 ts_skewness(close, 30)
    data_ts_skewness_close = ts_skewness(data['close'], 30)
    # 4. 计算 ts_delta(vwap, 10) * ts_weighted_decay(vol, 0.6) * ts_skewness(close, 30)
    data_multiply = multiply(data_ts_delta_vwap, data_ts_weighted_decay_vol, data_ts_skewness_close)
    # 5. 计算 ts_rank(ts_delta(vwap, 10) * ts_weighted_decay(vol, 0.6) * ts_skewness(close, 30), 60)
    factor = ts_rank(data_multiply, 60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()