import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, multiply, ts_delta

def factor_5970(data, **kwargs):
    """
    因子名称: PriceVolumeTrendSkew_71630
    数学表达式: ts_skewness(multiply(ts_delta(close, 3), vol), 10)
    中文描述: 该因子计算每日收盘价的3日变化值与当日成交量的乘积，然后计算这些乘积在过去10天的偏度。这结合了短期价格动量和成交量信息，并引入了偏度来衡量这种量价乘积分布的非对称性。正偏度可能表示在过去10天内，由交易量支持的较大价格上涨的频率和幅度大于同等程度的价格下跌；负偏度则反之。这可以用于捕捉短期内由市场活动驱动的价格趋势中，极端事件（如大涨或大跌）的影响程度和方向。
    因子应用场景：
    1. 趋势识别：通过量价关系的偏度来识别潜在的趋势反转点。
    2. 异常检测：识别量价行为中极端事件的发生。
    """
    # 1. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], 3)
    # 2. 计算 multiply(ts_delta(close, 3), vol)
    data_multiply = multiply(data_ts_delta_close, data['vol'])
    # 3. 计算 ts_skewness(multiply(ts_delta(close, 3), vol), 10)
    factor = ts_skewness(data_multiply, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()