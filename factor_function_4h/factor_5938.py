import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_skewness

def factor_5938(data, **kwargs):
    """
    因子名称: Volatility_Skew_Ratio_52357
    数学表达式: divide(ts_skewness(high, 10), ts_skewness(low, 5))
    中文描述: 该因子旨在捕捉高价和低价波动偏度的相对强弱。它通过计算过去10天最高价的偏度与过去5天最低价的偏度的比值来构建。高价偏度衡量了近期高价波动的对称性，正偏度表示存在较多极端高价，负偏度表示极端高价较少。低价偏度则反映了近期低价波动的对称性。将两者相除，可以观察到在高价和低价区域的波动特性差异。例如，如果高价偏度为正且低价偏度为负，比值可能为负，暗示市场在高位更容易出现极端上涨，而在低位更容易出现极端下跌，这可能预示着趋势的形成或延续。如果比值较高（正值），可能意味着高位存在更强的上涨动能或情绪，而低位相对稳定。如果比值较低（负值），可能意味着低位存在更强的下跌动能或恐慌，而高位相对疲软。这个因子结合了不同时间窗口（10天和5天）的偏度信息，相较于简单的Z分数比值，引入了对波动形态的考量，具有一定的创新性。可以用于识别市场情绪的非对称性波动，辅助判断趋势的强度和潜在反转点。
    因子应用场景：
    1. 波动特性差异：观察高价和低价区域的波动特性差异。
    2. 趋势识别：辅助判断趋势的强度和潜在反转点。
    3. 市场情绪分析：识别市场情绪的非对称性波动。
    """
    # 1. 计算 ts_skewness(high, 10)
    data_ts_skewness_high = ts_skewness(data['high'], d = 10)
    # 2. 计算 ts_skewness(low, 5)
    data_ts_skewness_low = ts_skewness(data['low'], d = 5)
    # 3. 计算 divide(ts_skewness(high, 10), ts_skewness(low, 5))
    factor = divide(data_ts_skewness_high, data_ts_skewness_low)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()