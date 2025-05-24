import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, divide, ts_sum, multiply, subtract

def factor_5687(data, **kwargs):
    """
    因子名称: volume_weighted_price_range_std_59949
    数学表达式: ts_std_dev(divide(ts_sum(multiply(vol, subtract(high, low)), 5), ts_sum(vol, 5)), 20)
    中文描述: 该因子计算过去20天内，5日成交量加权的价格范围（最高价-最低价）的标准差。它结合了成交量加权的价格波动和波动率的概念，旨在衡量市场在一段时间内的价格离散程度。创新之处在于，它不仅考虑了日内价格波动幅度，还通过成交量进行加权，并进一步计算其波动率，从而更全面地反映市场活跃度和价格稳定性的关系。适用于捕捉市场情绪变化和风险评估。
    因子应用场景：
    1. 市场情绪变化：标准差越高，表示市场情绪波动越大。
    2. 风险评估：可用于评估市场风险，标准差越高，风险越高。
    """
    # 1. 计算 subtract(high, low)
    data_subtract = subtract(data['high'], data['low'])
    # 2. 计算 multiply(vol, subtract(high, low))
    data_multiply = multiply(data['vol'], data_subtract)
    # 3. 计算 ts_sum(multiply(vol, subtract(high, low)), 5)
    data_ts_sum_multiply = ts_sum(data_multiply, 5)
    # 4. 计算 ts_sum(vol, 5)
    data_ts_sum_vol = ts_sum(data['vol'], 5)
    # 5. 计算 divide(ts_sum(multiply(vol, subtract(high, low)), 5), ts_sum(vol, 5))
    data_divide = divide(data_ts_sum_multiply, data_ts_sum_vol)
    # 6. 计算 ts_std_dev(divide(ts_sum(multiply(vol, subtract(high, low)), 5), ts_sum(vol, 5)), 20)
    factor = ts_std_dev(data_divide, 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()