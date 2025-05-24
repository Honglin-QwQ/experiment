import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, adv, ts_std_dev, divide

def factor_5987(data, **kwargs):
    """
    因子名称: Ranked_Volume_Volatility_Ratio_69106
    数学表达式: divide(ts_rank(adv(volume, 20), 26), ts_std_dev(volume, 20))
    中文描述: 该因子计算过去20天平均成交量在过去26天内的排名与过去20天成交量标准差的比值。它结合了参考因子中的时间序列排名和平均成交量概念，并引入了成交量波动性作为新的元素。高排名和低波动性可能表明成交量稳定且相对较高，而低排名和高波动性可能指示成交量不稳定且相对较低。这个因子可以用于识别具有稳定高交易活跃度的股票，或者捕捉交易量异常波动的信号。
    因子应用场景：
    1. 识别具有稳定高交易活跃度的股票。
    2. 捕捉交易量异常波动的信号。
    """
    # 1. 计算 adv(volume, 20)
    data_adv = adv(data['vol'], d = 20)
    # 2. 计算 ts_rank(adv(volume, 20), 26)
    data_ts_rank = ts_rank(data_adv, d = 26)
    # 3. 计算 ts_std_dev(volume, 20)
    data_ts_std_dev = ts_std_dev(data['vol'], d = 20)
    # 4. 计算 divide(ts_rank(adv(volume, 20), 26), ts_std_dev(volume, 20))
    factor = divide(data_ts_rank, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()