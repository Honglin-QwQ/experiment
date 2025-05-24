import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, multiply, ts_std_dev, ts_delta

def factor_5795(data, **kwargs):
    """
    数学表达式: divide(multiply(vwap, ts_std_dev(vwap, 5)), ts_delta(close, 1))
    中文描述: 该因子结合了VWAP、其短期波动性和价格动量。它计算VWAP与其短期（5天）标准差的乘积，再除以当日收盘价相对于前一日的变化。这个因子旨在捕捉价格在有成交量支持下的波动强度与短期价格变化的比率。较高的因子值可能表明在有成交量的情况下，价格波动相对当日价格变化更为剧烈，这可能预示着趋势的延续或反转。创新点在于将VWAP与波动性的乘积与短期价格动量相结合，提供了一个更全面的视角来评估价格行为。
    因子应用场景：
    1. 波动性分析：用于识别成交量加权平均价格的波动性与价格动量之间的关系，可以帮助分析师评估市场活跃程度和潜在的趋势变化。
    2. 趋势识别：较高的因子值可能预示着在成交量支持下的价格波动较为剧烈，可能暗示趋势的延续或反转。
    3. 量价关系研究：该因子结合了成交量和价格信息，有助于研究量价关系，从而更好地理解市场行为。
    """
    # 1. 计算 ts_std_dev(vwap, 5)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 5)
    # 2. 计算 multiply(vwap, ts_std_dev(vwap, 5))
    data_multiply = multiply(data['vwap'], data_ts_std_dev_vwap)
    # 3. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 4. 计算 divide(multiply(vwap, ts_std_dev(vwap, 5)), ts_delta(close, 1))
    factor = divide(data_multiply, data_ts_delta_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()