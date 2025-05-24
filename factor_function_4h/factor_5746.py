import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_std_dev, ts_corr, divide

def factor_5746(data, **kwargs):
    """
    因子名称: PriceVolumeVolatilityRankRatio_90791
    数学表达式: divide(ts_rank(ts_std_dev(close, 10), 20), ts_rank(ts_corr(close, vol, 15), 30))
    中文描述: 该因子计算收盘价在过去10天的标准差的时间序列排名与收盘价和交易量在过去15天的相关性的时间序列排名的比值。收盘价的标准差衡量价格波动性，其时间序列排名反映了当前波动性在过去一段时间内的相对水平。收盘价和交易量的相关性反映了价量关系的强度，其时间序列排名反映了当前价量相关性在过去一段时间内的相对水平。该因子通过比较波动性排名和价量相关性排名，旨在捕捉市场情绪和趋势的潜在变化。高值可能表示波动性相对较高而价量相关性相对较低，可能预示着趋势的疲软或反转；低值则可能表示波动性相对较低而价量相关性相对较高，可能预示着趋势的持续。创新点在于将价格波动性和价量相关性结合起来，并通过时间序列排名进行相对比较，提供了一个新的视角来评估市场状态。
    因子应用场景：
    1. 趋势反转识别：高因子值可能预示趋势疲软或反转。
    2. 趋势持续识别：低因子值可能预示趋势持续。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 2. 计算 ts_rank(ts_std_dev(close, 10), 20)
    data_ts_rank_std = ts_rank(data_ts_std_dev, 20)
    # 3. 计算 ts_corr(close, vol, 15)
    data_ts_corr = ts_corr(data['close'], data['vol'], 15)
    # 4. 计算 ts_rank(ts_corr(close, vol, 15), 30)
    data_ts_rank_corr = ts_rank(data_ts_corr, 30)
    # 5. 计算 divide(ts_rank(ts_std_dev(close, 10), 20), ts_rank(ts_corr(close, vol, 15), 30))
    factor = divide(data_ts_rank_std, data_ts_rank_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()