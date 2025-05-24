import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, floor, ts_mean, divide
import pandas as pd

def factor_5853(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(high, 6), floor(ts_mean(low, 6)))
    中文描述: 该因子旨在衡量短期价格波动相对于长期最低价地板值的比率。它结合了过去6天最高价的标准差（反映短期波动性）和过去6天最低价的平均值的向下取整（反映长期支撑或地板）。通过计算这两者的比率，该因子试图捕捉价格波动性在长期支撑水平附近的相对强度。当短期波动性相对于长期地板值较高时，可能预示着潜在的市场情绪变化或价格突破。创新点在于将短期波动性指标与长期价格地板概念结合，并使用地板函数对长期均值进行处理，增加其对整数位重要性的考量。
    因子应用场景：
    1. 波动性分析：用于识别短期波动性相对于长期支撑水平较高的股票，可能预示着潜在的价格波动或趋势变化。
    2. 支撑位评估：结合长期最低价地板值，评估当前价格波动是否接近或突破长期支撑位。
    3. 情绪指标：作为市场情绪的指标，当波动性相对于地板值较高时，可能反映市场情绪的不确定性或紧张。
    """
    # 1. 计算 ts_std_dev(high, 6)
    data_ts_std_dev_high = ts_std_dev(data['high'], 6)
    # 2. 计算 ts_mean(low, 6)
    data_ts_mean_low = ts_mean(data['low'], 6)
    # 3. 计算 floor(ts_mean(low, 6))
    data_floor_ts_mean_low = floor(data_ts_mean_low)
    # 4. 计算 divide(ts_std_dev(high, 6), floor(ts_mean(low, 6)))
    factor = divide(data_ts_std_dev_high, data_floor_ts_mean_low)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()