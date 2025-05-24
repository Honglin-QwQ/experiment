import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, ts_corr, inverse, rank

def factor_5834(data, **kwargs):
    """
    数学表达式: rank(ts_std_dev(ts_delta(volume, 3), 60)) - rank(ts_corr(close, inverse(vwap), 60))
    中文描述: 该因子结合了成交量变化和量加权平均价格的反转，旨在捕捉市场的波动性和趋势强度。首先，计算过去60天内3日成交量变化的标准差，并对其进行排名。高标准差排名表示成交量变化剧烈，可能预示着市场情绪的波动。其次，计算收盘价与量加权平均价格倒数在过去60天内的相关性，并对其进行排名。量加权平均价格倒数可以视为一种反向价格指标，与收盘价的相关性排名反映了价格趋势的持续性。最后，用成交量变化标准差的排名减去价格相关性的排名。当成交量变化剧烈且收盘价与反向VWAP的相关性较低时，因子值较高，可能指示着趋势的潜在反转或动量减弱。创新点在于结合了成交量变化的波动性与反向VWAP的价格相关性，从不同维度衡量市场状态，并使用排名进行标准化处理，增强了可比性。
    因子应用场景：
    1. 波动性分析：用于识别成交量波动较大的股票，可能预示着市场关注度高或存在潜在的交易机会。
    2. 趋势反转信号：当因子值较高时，可能预示着当前趋势的减弱或潜在的反转。
    3. 量价关系研究：通过结合成交量变化和价格关系，辅助分析量价之间的背离或协同效应。
    """
    # 1. 计算 ts_delta(volume, 3)
    data_ts_delta_volume = ts_delta(data['vol'], 3)
    # 2. 计算 ts_std_dev(ts_delta(volume, 3), 60)
    data_ts_std_dev = ts_std_dev(data_ts_delta_volume, 60)
    # 3. 计算 rank(ts_std_dev(ts_delta(volume, 3), 60))
    rank_volume_std = rank(data_ts_std_dev, 2)
    # 4. 计算 inverse(vwap)
    data_inverse_vwap = inverse(data['vwap'])
    # 5. 计算 ts_corr(close, inverse(vwap), 60)
    data_ts_corr = ts_corr(data['close'], data_inverse_vwap, 60)
    # 6. 计算 rank(ts_corr(close, inverse(vwap), 60))
    rank_price_corr = rank(data_ts_corr, 2)
    # 7. 计算 rank(ts_std_dev(ts_delta(volume, 3), 60)) - rank(ts_corr(close, inverse(vwap), 60))
    factor = rank_volume_std - rank_price_corr

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()