import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_mean, divide, ts_delta, rank, scale
import pandas as pd
import numpy as np

def factor_5724(data, **kwargs):
    """
    因子名称: VolHighMeanRatio_TSDelta_RankScale_74930
    数学表达式: scale(rank(ts_delta(divide(ts_mean(vol, 20), ts_mean(high, 20)), 30)))
    中文描述: 该因子在历史因子的基础上进行了改进，首先计算过去20天成交量均值与最高价均值的比值，该比值反映了在一段时间内，相对于价格高点，市场的交易活跃程度。然后计算该比值与30天前的该比值之差，捕捉其短期趋势变化。最后，对这个差值进行排名并标准化。创新点在于缩短了时间窗口，提高了对短期市场变化的敏感性，并引入了排名和标准化操作，以消除量纲影响，提高因子的稳定性和可比性。这可能有助于识别在短期内成交量相对于价格高点发生显著变化的股票。
    因子应用场景：
    1. 市场活跃度分析：用于衡量市场对特定股票的交易兴趣，成交量相对于价格高点越高，可能表明市场对该股票的兴趣越浓厚。
    2. 短期趋势跟踪：通过计算比率差值，可以捕捉市场情绪的短期变化，从而辅助判断股票价格的短期走势。
    3. 量化交易：结合排名和标准化，可以生成稳定的量化信号，用于构建交易策略。
    """
    # 1. 计算 ts_mean(vol, 20)
    data_ts_mean_vol = ts_mean(data['vol'], 20)
    # 2. 计算 ts_mean(high, 20)
    data_ts_mean_high = ts_mean(data['high'], 20)
    # 3. 计算 divide(ts_mean(vol, 20), ts_mean(high, 20))
    data_divide = divide(data_ts_mean_vol, data_ts_mean_high)
    # 4. 计算 ts_delta(divide(ts_mean(vol, 20), ts_mean(high, 20)), 30)
    data_ts_delta = ts_delta(data_divide, 30)
    # 5. 计算 rank(ts_delta(divide(ts_mean(vol, 20), ts_mean(high, 20)), 30))
    factor_rank = rank(data_ts_delta, 2)
    # 6. 计算 scale(rank(ts_delta(divide(ts_mean(vol, 20), ts_mean(high, 20)), 30)))
    factor = scale(factor_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()