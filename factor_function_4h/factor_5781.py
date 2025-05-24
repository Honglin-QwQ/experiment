import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_decay_linear, subtract, ts_rank, ts_std_dev, divide

def factor_5781(data, **kwargs):
    """
    因子名称: Decayed_Rank_Difference_Weighted_By_Volatility_25850
    数学表达式: divide(ts_decay_linear(subtract(ts_rank(high, 15), ts_rank(low, 15)), 7), ts_std_dev(close, 15))
    中文描述: 该因子计算过去15天内最高价排名与最低价排名之差的7天线性衰减平均值，并将其除以过去15天收盘价的标准差。它结合了时间序列排名、线性衰减和波动率的概念，旨在捕捉近期高低价相对强度的动态变化，并根据市场波动性进行调整。当分子较大且分母较小时，可能表明近期价格倾向于在高位且市场波动较小，显示出较强的上涨动能；反之，可能表明下行压力。相较于参考因子，创新点在于引入了高低价排名的差值作为基础，并用收盘价的标准差进行波动率调整，以及调整了时间窗口和衰减期，以期获得更好的预测能力和稳定性。
    因子应用场景：
    1. 动量分析：用于识别价格动量，高值可能表示上涨动能强劲。
    2. 波动率调整：通过波动率进行调整，使得因子在不同市场环境下的表现更为稳定。
    3. 高低价强度：捕捉高低价相对强度的变化，辅助判断趋势反转。
    """
    # 1. 计算 ts_rank(high, 15)
    data_ts_rank_high = ts_rank(data['high'], 15)
    # 2. 计算 ts_rank(low, 15)
    data_ts_rank_low = ts_rank(data['low'], 15)
    # 3. 计算 subtract(ts_rank(high, 15), ts_rank(low, 15))
    data_subtract = subtract(data_ts_rank_high, data_ts_rank_low)
    # 4. 计算 ts_decay_linear(subtract(ts_rank(high, 15), ts_rank(low, 15)), 7)
    data_ts_decay_linear = ts_decay_linear(data_subtract, 7)
    # 5. 计算 ts_std_dev(close, 15)
    data_ts_std_dev = ts_std_dev(data['close'], 15)
    # 6. 计算 divide(ts_decay_linear(subtract(ts_rank(high, 15), ts_rank(low, 15)), 7), ts_std_dev(close, 15))
    factor = divide(data_ts_decay_linear, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()