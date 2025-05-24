import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_skewness, ts_decay_exp_window, ts_std_dev

import pandas as pd

def factor_6084(data, **kwargs):
    """
    因子名称: VolumeVolatilitySkew_DecayRatio_28058
    数学表达式: divide(ts_skewness(vol, 30), ts_decay_exp_window(ts_std_dev(vol, 20), 90, factor=0.15))
    中文描述: 该因子旨在捕捉短期成交量分布的偏度相对于长期成交量波动率指数衰减加权平均值的比值。ts_skewness(vol, 30)计算过去30天成交量的偏度，衡量成交量分布的对称性。ts_decay_exp_window(ts_std_dev(vol, 20), 90, factor=0.15)计算过去90天内，20日成交量标准差的指数衰减加权平均值，反映长期加权的成交量波动性趋势。通过计算这两者的比值，该因子试图识别成交量分布的偏态变化是否与长期加权波动性趋势存在特定关系。创新点在于结合了成交量的偏度（非标准差）与长期加权波动率，并使用比值来衡量这种关系，同时引入了不同的时间窗口和衰减因子参数，以期捕捉更复杂的成交量动态。
    因子应用场景：
    1. 识别成交量偏度与长期波动率趋势的关系：用于识别成交量分布的偏态变化是否与长期加权波动性趋势存在特定关系。
    2. 市场情绪分析：成交量偏度可能反映市场情绪，与长期波动率结合可以更全面地评估市场风险。
    """
    # 1. 计算 ts_skewness(vol, 30)
    data_ts_skewness = ts_skewness(data['vol'], d=30)
    # 2. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev = ts_std_dev(data['vol'], d=20)
    # 3. 计算 ts_decay_exp_window(ts_std_dev(vol, 20), 90, factor=0.15)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_std_dev, d=90, factor=0.15)
    # 4. 计算 divide(ts_skewness(vol, 30), ts_decay_exp_window(ts_std_dev(vol, 20), 90, factor=0.15))
    factor = divide(data_ts_skewness, data_ts_decay_exp_window)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()