import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_min_max_diff

def factor_5750(data, **kwargs):
    """
    因子名称: TS_MinMaxDiff_ZScore_Close_91221
    数学表达式: ts_zscore(ts_min_max_diff(close, 10, f=0.8), 5)
    中文描述: 该因子首先计算收盘价在过去10天内的最小值与最大值之和的0.8倍与当前收盘价的差值，然后计算该差值在过去5天内的Z分数。这结合了短期价格极值的相对位置信息和其在近期波动中的标准化表现，旨在捕捉价格在短期极值区间内的相对强弱和动量，可能用于识别超买超卖或趋势反转信号。相较于参考因子，创新点在于引入了ts_min_max_diff运算符，结合了最小值和最大值的信息，并在此基础上进行了Z分数标准化，提供了更丰富的价格波动特征描述。
    因子应用场景：
    1. 超买超卖识别：当因子值较高时，可能表明股票处于超买状态；反之，较低时可能表明处于超卖状态。
    2. 趋势反转信号：因子值的快速变化可能预示着趋势的反转。
    3. 动量捕捉：通过结合价格极值和Z分数，因子能够捕捉短期内的价格动量。
    """
    # 1. 计算 ts_min_max_diff(close, 10, f=0.8)
    data_ts_min_max_diff = ts_min_max_diff(data['close'], d=10, f=0.8)
    # 2. 计算 ts_zscore(ts_min_max_diff(close, 10, f=0.8), 5)
    factor = ts_zscore(data_ts_min_max_diff, d=5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()