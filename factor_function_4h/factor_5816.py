import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, multiply, divide

def factor_5816(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(multiply(close, ts_delta(vol, 5)), 20), ts_std_dev(ts_delta(close, 3), 90))
    中文描述: 该因子计算了短期成交量加权价格变化的标准差与长期价格变化标准差的比值。短期窗口期为20天，长期窗口期为90天。分子中的成交量加权价格变化通过将收盘价与前5日成交量的差值相乘得到，反映了短期内价格变化与成交量变动的联合波动性。分母计算了长期收盘价3日变化的波动性。该因子的创新点在于结合了成交量变动来衡量短期价格变化的波动性，并将其与纯粹的长期价格变化波动性进行比较。较高的因子值可能表明短期内价格变化伴随着较高的成交量变动，且波动性较大，而纯粹的长期价格变化波动性相对稳定。这可以用于识别短期内由成交量变动驱动的异常价格波动。相较于历史因子，该因子将偏度替换为标准差，降低了对异常值的敏感性，并调整了时间窗口参数，以期获得更稳定的预测能力。
    因子应用场景：
    1. 异常波动识别：用于识别短期内由成交量变动驱动的异常价格波动。
    2. 市场情绪分析：较高的因子值可能表明市场情绪不稳定，成交量变动对价格的影响较大。
    """

    # 1. 计算 ts_delta(vol, 5)
    data_ts_delta_vol = ts_delta(data['vol'], 5)

    # 2. 计算 multiply(close, ts_delta(vol, 5))
    data_multiply_close_ts_delta_vol = multiply(data['close'], data_ts_delta_vol)

    # 3. 计算 ts_std_dev(multiply(close, ts_delta(vol, 5)), 20)
    data_ts_std_dev_numerator = ts_std_dev(data_multiply_close_ts_delta_vol, 20)

    # 4. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], 3)

    # 5. 计算 ts_std_dev(ts_delta(close, 3), 90)
    data_ts_std_dev_denominator = ts_std_dev(data_ts_delta_close, 90)

    # 6. 计算 divide(ts_std_dev(multiply(close, ts_delta(vol, 5)), 20), ts_std_dev(ts_delta(close, 3), 90))
    factor = divide(data_ts_std_dev_numerator, data_ts_std_dev_denominator)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()