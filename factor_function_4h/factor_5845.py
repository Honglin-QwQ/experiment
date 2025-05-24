import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, abs, subtract, round, ts_mean, divide

def factor_5845(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Roundness_Ratio_88632
    数学表达式: divide(ts_std_dev(vwap, 22), abs(subtract(round(close), ts_mean(close, 22))))
    中文描述: 该因子计算过去22天VWAP的标准差与当前收盘价四舍五入值与其过去22天收盘价均值差的绝对值的比值。它结合了VWAP的波动性信息和收盘价的“整数回归”特性。当VWAP波动较大，且收盘价远离其近期均值并接近整数关口时，因子值可能较高。这可能用于识别价格波动与心理整数关口效应叠加的市场状态，寻找潜在的交易机会。创新点在于结合了时间序列统计量（标准差、均值）和基于心理层面的整数回归概念（round(close)），并构建了一个比值来衡量这两者的相对强度。
    因子应用场景：
    1. 识别价格波动与心理整数关口效应叠加的市场状态。
    2. 寻找潜在的交易机会。
    """
    # 1. 计算 ts_std_dev(vwap, 22)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 22)
    # 2. 计算 round(close)
    data_round_close = round(data['close'])
    # 3. 计算 ts_mean(close, 22)
    data_ts_mean_close = ts_mean(data['close'], 22)
    # 4. 计算 subtract(round(close), ts_mean(close, 22))
    data_subtract = subtract(data_round_close, data_ts_mean_close)
    # 5. 计算 abs(subtract(round(close), ts_mean(close, 22)))
    data_abs = abs(data_subtract)
    # 6. 计算 divide(ts_std_dev(vwap, 22), abs(subtract(round(close), ts_mean(close, 22))))
    factor = divide(data_ts_std_dev_vwap, data_abs)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()