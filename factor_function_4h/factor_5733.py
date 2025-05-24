import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_arg_max, ts_corr, ts_std_dev

def factor_5733(data, **kwargs):
    """
    数学表达式: ts_arg_max(ts_corr(vol, ts_std_dev(close, 10), 20), 15)
    中文描述: 该因子通过结合成交量与收盘价波动率的相关性及其在时间序列上的最大值位置来捕捉市场情绪和潜在的价格转折点。首先计算过去20天内成交量与过去10天收盘价标准差（衡量波动率）的滚动相关性。然后，找到这个滚动相关性在过去15天内达到最大值的相对位置（0表示当天，1表示前一天，以此类推）。该因子值反映了当前市场成交量与波动率同步性相对于近期历史的强度和持续性。较高的因子值（索引较小）可能表明近期成交量与波动率的同步性达到高峰，可能预示着趋势的延续或反转。相较于参考因子仅使用成交量均值或最低价/收盘价的位置信息，本因子创新性地结合了成交量和波动率的动态关系，并利用时间序列最大值位置来捕捉这种关系的极值点，为市场分析提供了更丰富的视角。
    因子应用场景：
    1. 市场情绪分析： 通过成交量和波动率的相关性，可以判断市场是处于恐慌抛售还是乐观买入状态。
    2. 价格转折点预测： 当成交量与波动率的同步性达到高峰时，可能预示着趋势的结束或反转。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 2. 计算 ts_corr(vol, ts_std_dev(close, 10), 20)
    data_ts_corr = ts_corr(data['vol'], data_ts_std_dev, 20)
    # 3. 计算 ts_arg_max(ts_corr(vol, ts_std_dev(close, 10), 20), 15)
    factor = ts_arg_max(data_ts_corr, 15)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()