import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, divide, ts_delta, ts_std_dev

def factor_5716(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Skew_62475
    数学表达式: ts_skewness(divide(ts_delta(vwap, 10), ts_std_dev(vwap, 20)), 60)
    中文描述: 该因子旨在捕捉VWAP短期动量相对于其短期波动性的偏度。首先计算VWAP在10天内的变化量，并将其除以VWAP在20天内的标准差，得到一个波动性调整后的短期动量信号。然后，计算这个波动性调整后的动量信号在过去60天内的偏度。正偏度可能表明近期存在一些大的正向波动，而负偏度可能表明存在大的负向波动。这个因子结合了短期动量、短期波动性和长期偏度，试图识别那些在波动性调整后的动量分布上存在异常偏斜的股票。创新点在于计算波动性调整后动量的偏度，以捕捉更深层次的市场情绪和行为特征，并根据历史评估结果，缩短了delta和std_dev的窗口期，并引入了ts_skewness操作符，以期提升因子的预测能力和稳定性。
    因子应用场景：
    1. 波动性异常检测：识别波动性调整后的动量分布存在异常偏斜的股票。
    2. 市场情绪分析：捕捉市场情绪和行为特征。
    3. 短期趋势预测：正偏度可能表明近期存在一些大的正向波动，而负偏度可能表明存在大的负向波动。
    """
    # 1. 计算 ts_delta(vwap, 10)
    data_ts_delta_vwap = ts_delta(data['vwap'], 10)
    # 2. 计算 ts_std_dev(vwap, 20)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 20)
    # 3. 计算 divide(ts_delta(vwap, 10), ts_std_dev(vwap, 20))
    data_divide = divide(data_ts_delta_vwap, data_ts_std_dev_vwap)
    # 4. 计算 ts_skewness(divide(ts_delta(vwap, 10), ts_std_dev(vwap, 20)), 60)
    factor = ts_skewness(data_divide, 60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()