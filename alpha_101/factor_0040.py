import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import sqrt, subtract, multiply

def factor_0040(data, **kwargs):
    """
    数学表达式: (((high * low)^0.5) - vwap)
    中文描述: 该因子计算的是每日最高价和最低价乘积的平方根，再减去当日的成交量加权平均价，反映了价格波动幅度相对于成交均价的偏离程度，可以用于捕捉日内价格异常波动；
    应用场景包括：
    1. 识别日内高波动股票，用于高频交易或日内趋势跟踪策略；
    2. 作为异常检测指标，筛选出价格波动与成交量不匹配的股票；
    3. 结合其他量价因子，构建更复杂的量化交易模型，例如加入动量因子或反转因子。
    """
    # 1. 计算 high * low
    high_low_product = multiply(data['high'], data['low'])
    # 2. 计算 (high * low)^0.5
    sqrt_high_low_product = sqrt(high_low_product)
    # 3. 计算 ((high * low)^0.5) - vwap
    factor = subtract(sqrt_high_low_product, data['vwap'])

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()