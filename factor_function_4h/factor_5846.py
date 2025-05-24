import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, divide, ts_std_dev, ts_arg_max, ts_corr, multiply

def factor_5846(data, **kwargs):
    """
    因子名称: VolumeWeightedPrice_VolatilityRatio_ARGMAX_Enhanced_31885
    数学表达式: multiply(rank(divide(ts_std_dev(vwap, 30), ts_std_dev(amount, 30))), ts_arg_max(ts_corr(vwap, vol, 90), 120))
    中文描述: 该因子是基于历史输出的改进版本，旨在增强预测能力和降低波动性。它首先计算过去30天VWAP标准差与过去30天交易额标准差的比值的排名，以更稳定地衡量价格波动与交易活动波动的相对强度。然后，计算过去90天VWAP与交易量的相关性，并找到过去120天内该相关性的最大值出现的相对位置。最终因子值为前两者的乘积。相较于原因子，该因子通过增加时间窗口长度来平滑波动，并引入rank操作符对波动率比值进行排序，以消除量纲差异并提高鲁棒性。高因子值可能表明在相对稳定的价格和交易活动波动下，存在一个较强的、持续一段时间的价量相关性趋势，并且该趋势在近期达到了一个峰值，可能预示着动量或潜在的反转机会。
    因子应用场景：
    1. 波动性分析：用于衡量价格波动与交易活动波动的相对强度。
    2. 价量关系分析：用于识别价量相关性趋势及其峰值。
    3. 动量或反转机会识别：高因子值可能预示着动量或潜在的反转机会。
    """
    # 1. 计算 ts_std_dev(vwap, 30)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 30)
    # 2. 计算 ts_std_dev(amount, 30)
    data_ts_std_dev_amount = ts_std_dev(data['amount'], 30)
    # 3. 计算 divide(ts_std_dev(vwap, 30), ts_std_dev(amount, 30))
    data_divide = divide(data_ts_std_dev_vwap, data_ts_std_dev_amount)
    # 4. 计算 rank(divide(ts_std_dev(vwap, 30), ts_std_dev(amount, 30)))
    data_rank = rank(data_divide, 2)
    # 5. 计算 ts_corr(vwap, vol, 90)
    data_ts_corr = ts_corr(data['vwap'], data['vol'], 90)
    # 6. 计算 ts_arg_max(ts_corr(vwap, vol, 90), 120)
    data_ts_arg_max = ts_arg_max(data_ts_corr, 120)
    # 7. 计算 multiply(rank(divide(ts_std_dev(vwap, 30), ts_std_dev(amount, 30))), ts_arg_max(ts_corr(vwap, vol, 90), 120))
    factor = multiply(data_rank, data_ts_arg_max)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()