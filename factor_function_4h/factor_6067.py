import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, multiply, ts_median, divide

def factor_6067(data, **kwargs):
    """
    因子名称: VolWeightedPriceVolatilityRatio_85470
    数学表达式: divide(ts_std_dev(multiply(close, vol), 120), ts_median(multiply(close, vol), 60))
    中文描述: 该因子通过计算收盘价与成交量乘积（代表成交额的近似值）的长期标准差与中期中位数之比来衡量市场的波动性和趋势。分子采用120天的标准差，捕捉较长时间内的成交额波动性；分母采用60天的中位数，提供一个中期稳定的成交额水平参考。这个比值可以反映当前市场的波动性相对于中期平均水平的高低。高值可能表明市场波动加剧或趋势变化加速，低值可能表明市场相对稳定或趋势减弱。相较于参考因子，该因子结合了价格和成交量信息，并使用了标准差和中位数两种不同的统计量，以及不同长度的时间窗口，以更全面地捕捉市场动态。
    因子应用场景：
    1. 波动性衡量：用于衡量市场成交额的波动程度。
    2. 趋势判断：辅助判断市场趋势的强度和变化。
    """
    # 1. 计算 multiply(close, vol)
    close_vol = multiply(data['close'], data['vol'])
    # 2. 计算 ts_std_dev(multiply(close, vol), 120)
    std_dev = ts_std_dev(close_vol, 120)
    # 3. 计算 ts_median(multiply(close, vol), 60)
    median = ts_median(close_vol, 60)
    # 4. 计算 divide(ts_std_dev(multiply(close, vol), 120), ts_median(multiply(close, vol), 60))
    factor = divide(std_dev, median)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()