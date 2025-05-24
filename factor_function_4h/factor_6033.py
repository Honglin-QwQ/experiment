import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_delta, ts_std_dev, ts_delay, rank

def factor_6033(data, **kwargs):
    """
    因子名称: PriceVolatilityMomentum_17266
    数学表达式: ts_corr(ts_delta(close, 5), ts_std_dev(close, 20), 60) * ts_delay(rank(vol), 90)
    中文描述: 该因子结合了价格变化、价格波动率以及长期成交量排名信息，旨在捕捉价格动量与波动率之间的关系，并引入历史成交量排名作为辅助信号。
            因子表达式首先计算过去5天收盘价变化与过去20天收盘价标准差在过去60天内的相关性，然后将此相关性乘以90天前成交量的排名。
            这是一种创新的尝试，通过结合短期价格动态与长期成交量行为，识别潜在的交易机会。高相关性可能表明价格变化与波动率同步，而历史成交量排名则提供了市场活跃度的长期视角。
    因子应用场景：
    1. 趋势识别：用于识别价格动量与波动率之间的关系，结合成交量排名辅助判断趋势的可靠性。
    2. 市场活跃度分析：结合成交量排名，评估市场对价格动量和波动率变化的反应程度。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 2. 计算 ts_std_dev(close, 20)
    data_ts_std_dev_close = ts_std_dev(data['close'], 20)
    # 3. 计算 ts_corr(ts_delta(close, 5), ts_std_dev(close, 20), 60)
    data_ts_corr = ts_corr(data_ts_delta_close, data_ts_std_dev_close, 60)
    # 4. 计算 rank(vol)
    data_rank_vol = rank(data['vol'])
    # 5. 计算 ts_delay(rank(vol), 90)
    data_ts_delay_rank_vol = ts_delay(data_rank_vol, 90)
    # 6. 计算 ts_corr(ts_delta(close, 5), ts_std_dev(close, 20), 60) * ts_delay(rank(vol), 90)
    factor = data_ts_corr * data_ts_delay_rank_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()