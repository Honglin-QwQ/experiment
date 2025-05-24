import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, divide, ts_rank, ts_std_dev, subtract
import pandas as pd
import numpy as np

def factor_6066(data, **kwargs):
    """
    数学表达式: scale(divide(ts_rank(vol, 30), ts_std_dev(divide(subtract(high, low), close), 20)))
    中文描述: 该因子是基于对历史因子评估报告的分析和改进建议生成的。原始因子与收益率呈微弱负相关，且统计显著性较差。改进后的因子旨在捕捉成交量在短期窗口内的相对活跃度与标准化日内价格波动率之间的关系。因子表达式为：scale(divide(ts_rank(vol, 30), ts_std_dev(divide(subtract(high, low), close), 20)))。其中，ts_rank(vol, 30)计算过去30天成交量的时间序列排名，用于衡量短期交易活跃度，将窗口期从87缩短到30，以捕捉更近期的市场情绪。ts_std_dev(divide(subtract(high, low), close), 20)计算过去20天日内价格波动率（(high-low)/close）的标准差，用于衡量日内价格波动的稳定性。将成交量排名除以价格波动率的标准差，旨在识别在相对活跃的交易环境下，价格波动是否稳定。最后使用scale操作符对结果进行缩放，以便于比较和使用。创新点在于结合了短期成交量排名和标准化日内价格波动率，并根据历史评估结果调整了时间窗口，试图发现更有效的量价关系模式。
    因子应用场景：
    1. 量价关系分析：该因子可用于识别成交量活跃但价格波动稳定的股票，可能预示着市场对该股票的兴趣较高，但价格尚未出现剧烈波动。
    2. 风险评估：通过观察成交量排名与价格波动率之间的关系，可以评估股票的风险水平。较高的成交量排名和较低的价格波动率可能表明风险较低。
    """
    # 1. 计算 ts_rank(vol, 30)
    data_ts_rank_vol = ts_rank(data['vol'], 30)
    # 2. 计算 subtract(high, low)
    data_subtract_high_low = subtract(data['high'], data['low'])
    # 3. 计算 divide(subtract(high, low), close)
    data_divide_subtract_close = divide(data_subtract_high_low, data['close'])
    # 4. 计算 ts_std_dev(divide(subtract(high, low), close), 20)
    data_ts_std_dev = ts_std_dev(data_divide_subtract_close, 20)
    # 5. 计算 divide(ts_rank(vol, 30), ts_std_dev(divide(subtract(high, low), close), 20))
    data_divide = divide(data_ts_rank_vol, data_ts_std_dev)
    # 6. 计算 scale(divide(ts_rank(vol, 30), ts_std_dev(divide(subtract(high, low), close), 20)))
    factor = scale(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()