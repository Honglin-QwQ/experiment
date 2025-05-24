import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, ts_std_dev, ts_corr, ts_arg_max, multiply

def factor_5832(data, **kwargs):
    """
    因子名称: VolumeWeightedPrice_VolatilityRatio_ARGMAX_37681
    数学表达式: divide(ts_std_dev(vwap, 20), ts_std_dev(amount, 20)) * ts_arg_max(ts_corr(vwap, vol, 60), 90)
    中文描述: 该因子结合了VWAP、交易额和交易量的波动性与相关性信息。首先，计算过去20天VWAP的标准差与过去20天交易额标准差的比值，衡量价格波动与交易活动波动的相对强度。然后，计算过去60天VWAP与交易量的相关性，并找到过去90天内该相关性的最大值出现的相对位置。最终因子值为前两者的乘积。创新的地方在于结合了不同时间窗口的波动性和相关性信息，并通过时间序列最大值位置来捕捉趋势的持续性或反转信号。高因子值可能表明在价格和交易活动波动相对较高的情况下，存在一个较强的、持续一段时间的价量相关性趋势，并且该趋势在近期达到了一个峰值，可能预示着动量或潜在的反转机会。
    因子应用场景：
    1. 波动性分析：衡量价格波动与交易活动波动的相对强度。
    2. 相关性分析：捕捉价量相关性趋势的峰值。
    3. 趋势识别：识别动量或潜在的反转机会。
    """
    # 1. 计算 ts_std_dev(vwap, 20)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 20)
    # 2. 计算 ts_std_dev(amount, 20)
    data_ts_std_dev_amount = ts_std_dev(data['amount'], 20)
    # 3. 计算 divide(ts_std_dev(vwap, 20), ts_std_dev(amount, 20))
    data_divide = divide(data_ts_std_dev_vwap, data_ts_std_dev_amount)
    # 4. 计算 ts_corr(vwap, vol, 60)
    data_ts_corr = ts_corr(data['vwap'], data['vol'], 60)
    # 5. 计算 ts_arg_max(ts_corr(vwap, vol, 60), 90)
    data_ts_arg_max = ts_arg_max(data_ts_corr, 90)
    # 6. 计算 divide(ts_std_dev(vwap, 20), ts_std_dev(amount, 20)) * ts_arg_max(ts_corr(vwap, vol, 60), 90)
    factor = multiply(data_divide, data_ts_arg_max)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()