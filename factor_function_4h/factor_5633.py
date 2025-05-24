import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, reverse, rank, ts_std_dev, ts_corr, subtract, multiply

def factor_5633(data, **kwargs):
    """
    因子名称: factor_0002_36156
    数学表达式: reverse(rank(ts_delta(close, 5))) * ts_std_dev(vol, 15) - rank(ts_corr(high, low, 10))
    中文描述: 该因子是历史因子factor_0001的改进版本，旨在捕捉短期价格反转和交易量波动之间的关系，并考虑最高价与最低价的相关性。
            首先，计算收盘价5日的变化率，取反并进行排序，捕捉短期价格反转的动量。
            然后，计算过去15天成交量的标准差，反映市场流动性的变化。
            最后，减去最高价与最低价在过去10天内的相关性排名，用于衡量价格波动的一致性。
            相比于历史因子，该因子反转了价格变化方向，并使用成交量标准差代替平均成交量，旨在识别具有短期价格反转动量、高流动性波动且价格波动趋势一致的股票。
    因子应用场景：
    1. 短期价格反转：捕捉短期价格下跌后可能出现的反弹机会。
    2. 交易量波动性：识别交易量波动较大的股票，这些股票可能更具投机性。
    3. 价格波动一致性：衡量最高价与最低价的相关性，用于判断价格波动趋势是否一致。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 2. 计算 rank(ts_delta(close, 5))
    data_rank_ts_delta = rank(data_ts_delta)
    # 3. 计算 reverse(rank(ts_delta(close, 5)))
    data_reverse_rank_ts_delta = reverse(data_rank_ts_delta)
    # 4. 计算 ts_std_dev(vol, 15)
    data_ts_std_dev = ts_std_dev(data['vol'], 15)
    # 5. 计算 reverse(rank(ts_delta(close, 5))) * ts_std_dev(vol, 15)
    data_multiply = multiply(data_reverse_rank_ts_delta, data_ts_std_dev)
    # 6. 计算 ts_corr(high, low, 10)
    data_ts_corr = ts_corr(data['high'], data['low'], 10)
    # 7. 计算 rank(ts_corr(high, low, 10))
    data_rank_ts_corr = rank(data_ts_corr)
    # 8. 计算 reverse(rank(ts_delta(close, 5))) * ts_std_dev(vol, 15) - rank(ts_corr(high, low, 10))
    factor = subtract(data_multiply, data_rank_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()