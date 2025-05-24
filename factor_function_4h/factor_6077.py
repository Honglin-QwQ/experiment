import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, subtract, ts_skewness

def factor_6077(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(subtract(high, low), 10), ts_skewness(close, 10))
    中文描述: 该因子旨在捕捉价格波动性和收盘价偏度之间的关系。它计算过去10天最高价和最低价差值（反映日内波动性）的标准差，并将其除以过去10天收盘价的偏度。当波动性标准差较高且收盘价偏度为负（表明价格下跌时波动更大）时，因子值可能为负且绝对值较大，可能预示着市场恐慌或潜在的底部。反之，当波动性标准差较低且收盘价偏度为正（表明价格上涨时波动更大）时，因子值可能为正，可能预示着市场乐观或潜在的顶部。创新点在于结合了价格波动性的长期趋势（通过标准差衡量）和收盘价的短期偏度，试图从不同维度捕捉市场情绪和价格动态。
    因子应用场景：
    1. 市场情绪分析：该因子可用于识别市场情绪，例如，负值可能表示市场恐慌，正值可能表示市场乐观。
    2. 趋势反转预测：通过观察因子值的变化，可以尝试预测市场趋势的反转点。
    3. 风险管理：该因子可以帮助评估市场风险，例如，高波动性和负偏度可能预示着较高的下行风险。
    """
    # 1. 计算 subtract(high, low)
    data_subtract = subtract(data['high'], data['low'])
    # 2. 计算 ts_std_dev(subtract(high, low), 10)
    data_ts_std_dev = ts_std_dev(data_subtract, 10)
    # 3. 计算 ts_skewness(close, 10)
    data_ts_skewness = ts_skewness(data['close'], 10)
    # 4. 计算 divide(ts_std_dev(subtract(high, low), 10), ts_skewness(close, 10))
    factor = divide(data_ts_std_dev, data_ts_skewness)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()