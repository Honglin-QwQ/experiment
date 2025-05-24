import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, ts_std_dev, multiply, ts_decay_exp_window

def factor_5721(data, **kwargs):
    """
    因子名称: VolumePriceVolatilityRatio_Improved_27739
    数学表达式: divide(ts_std_dev(multiply(vol, ts_decay_exp_window(close, 10, factor=0.7)), 10), ts_std_dev(divide(high, low), 10))
    中文描述: 该因子是 VolumePriceVolatilityRatio 因子的改进版本。它计算了成交量与收盘价的指数衰减加权平均值乘积在过去10天的标准差，并将其除以最高价与最低价比值在过去10天的标准差。与原因子不同的是，分子部分引入了指数衰减加权平均（ts_decay_exp_window）来处理收盘价，使得近期收盘价对波动性计算的影响更大，从而更好地捕捉近期市场动态。分母仍然反映日内价格波动的波动性。通过计算这两个波动性指标的比值，该因子旨在捕捉成交额波动相对于日内价格波动波动性的相对强弱，并更加强调近期价格信息。高因子值可能表明近期成交额波动剧烈，而日内价格波动相对稳定，反之亦然。这可以用于识别市场情绪、流动性或潜在的价格趋势变化。该因子创新性在于在原因子基础上，通过引入指数衰减加权平均来优化收盘价的处理，增强了因子对近期市场变化的敏感性。
    因子应用场景：
    1. 市场情绪识别：高因子值可能表明近期成交额波动剧烈，而日内价格波动相对稳定，这可能反映了市场情绪的不稳定。
    2. 流动性分析：该因子可以帮助识别流动性变化，成交额波动相对于日内价格波动的波动性变化可能预示着流动性的变化。
    3. 潜在价格趋势变化：因子值的变化可能预示着潜在的价格趋势变化，通过分析因子值的历史表现，可以辅助判断价格趋势。
    """
    # 1. 计算 ts_decay_exp_window(close, 10, factor=0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data['close'], 10, factor=0.7)
    # 2. 计算 multiply(vol, ts_decay_exp_window(close, 10, factor=0.7))
    data_multiply = multiply(data['vol'], data_ts_decay_exp_window)
    # 3. 计算 ts_std_dev(multiply(vol, ts_decay_exp_window(close, 10, factor=0.7)), 10)
    data_ts_std_dev_numerator = ts_std_dev(data_multiply, 10)
    # 4. 计算 divide(high, low)
    data_divide = divide(data['high'], data['low'])
    # 5. 计算 ts_std_dev(divide(high, low), 10)
    data_ts_std_dev_denominator = ts_std_dev(data_divide, 10)
    # 6. 计算 divide(ts_std_dev(multiply(vol, ts_decay_exp_window(close, 10, factor=0.7)), 10), ts_std_dev(divide(high, low), 10))
    factor = divide(data_ts_std_dev_numerator, data_ts_std_dev_denominator)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()