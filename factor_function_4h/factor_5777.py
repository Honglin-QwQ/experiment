import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, multiply

def factor_5777(data, **kwargs):
    """
    因子名称: Volume_Price_Volatility_Ratio_20111
    数学表达式: divide(ts_std_dev(multiply(vol, close), 10), ts_std_dev(close, 10))
    中文描述: 该因子计算过去10天内成交量加权收盘价标准差与收盘价标准差的比值。它衡量了成交量对价格波动的影响程度。高值可能表示成交量在推动价格波动中扮演了更重要的角色，而低值可能表明价格波动更多是由其他因素驱动。这可以用于识别市场情绪和交易活动对价格稳定性的影响。
    因子应用场景：
    1. 市场情绪识别：高值可能表示市场情绪高涨，成交量放大推动价格波动。
    2. 交易活动分析：评估交易活动对价格稳定性的影响，高值可能表示交易活动对价格波动有较大影响。
    """
    # 1. 计算 multiply(vol, close)
    data_multiply = multiply(data['vol'], data['close'])
    # 2. 计算 ts_std_dev(multiply(vol, close), 10)
    data_ts_std_dev_1 = ts_std_dev(data_multiply, 10)
    # 3. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_2 = ts_std_dev(data['close'], 10)
    # 4. 计算 divide(ts_std_dev(multiply(vol, close), 10), ts_std_dev(close, 10))
    factor = divide(data_ts_std_dev_1, data_ts_std_dev_2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()