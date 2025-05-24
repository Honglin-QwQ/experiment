import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, multiply, ts_delta, rank, ts_std_dev

def factor_5814(data, **kwargs):
    """
    因子名称: Volume_Price_Interaction_Skew_92750
    数学表达式: ts_skewness(multiply(ts_delta(vol, 3), ts_delta(close, 3)), 20) * rank(ts_std_dev(close, 10))
    中文描述: 该因子旨在捕捉交易量变化与收盘价变化之间相互作用的非对称性，并结合价格波动性的排名。它首先计算过去3天交易量和收盘价的差值，并将两者相乘，得到一个衡量价量同步变化的指标。然后计算这个指标在过去20天内的偏度，以反映价量同步变化的分布是否偏斜。最后，将这个偏度乘以过去10天收盘价标准差的排名。高偏度和高价格波动性排名可能预示着在价格波动剧烈的时期，价量同步变化出现了显著的非对称性，这可能捕捉到市场情绪的极端变化或潜在的趋势反转信号。相对于参考因子，该因子创新性地将交易量变化和价格变化进行乘积操作，以捕捉它们之间的联合动态，并使用偏度来衡量这种联合动态的非线性特征，同时结合价格波动性排名，旨在提高因子的预测能力和对市场极端情况的敏感性。相较于历史输出，该因子不再单独关注交易量，而是将交易量和价格变化结合，并调整了时间窗口，希望能捕捉到更有效的市场信息。
    因子应用场景：
    1. 捕捉市场情绪的极端变化或潜在的趋势反转信号。
    2. 适用于价格波动剧烈的时期，捕捉价量同步变化的非对称性。
    """
    # 1. 计算 ts_delta(vol, 3)
    data_ts_delta_vol = ts_delta(data['vol'], 3)
    # 2. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], 3)
    # 3. 计算 multiply(ts_delta(vol, 3), ts_delta(close, 3))
    data_multiply = multiply(data_ts_delta_vol, data_ts_delta_close)
    # 4. 计算 ts_skewness(multiply(ts_delta(vol, 3), ts_delta(close, 3)), 20)
    data_ts_skewness = ts_skewness(data_multiply, 20)
    # 5. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 6. 计算 rank(ts_std_dev(close, 10))
    data_rank = rank(data_ts_std_dev, 2)
    # 7. 计算 ts_skewness(multiply(ts_delta(vol, 3), ts_delta(close, 3)), 20) * rank(ts_std_dev(close, 10))
    factor = data_ts_skewness * data_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()