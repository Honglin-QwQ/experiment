import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, divide, ts_delta, ts_mean, multiply

def factor_5704(data, **kwargs):
    """
    因子名称: Skewed_Momentum_Volume_Ratio_10309
    数学表达式: multiply(ts_skewness(returns, 30), divide(ts_delta(close, 10), ts_mean(vol, 60)))
    中文描述: 该因子旨在捕捉收益率的偏度与价格动量和长期成交量比率的结合效应。首先，计算过去30天收益率的偏度，以捕捉收益率分布的非对称性。然后，计算收盘价在10天内的变化（短期动量），并将其除以过去60天的平均成交量。最后，将这两部分相乘。相较于参考因子，创新点在于：1. 引入了收益率偏度，并调整了其计算窗口。2. 将短期价格动量与长期平均成交量进行比值，而非简单的相乘或取倒数，这可能更好地反映价格变化相对于市场活跃度的强度。3. 简化了价格变化部分的计算逻辑，直接使用ts_delta而非复杂的差值。该因子可能适用于识别那些收益率分布有特定偏向、短期动量强劲且相对于其长期平均水平成交量相对较低的股票。
    因子应用场景：
    1. 捕捉收益率偏度与量价关系：适用于寻找收益率分布不对称，同时短期动量与长期成交量比率异常的股票。
    2. 动量分析：识别短期价格动量强劲，但成交量相对较低的股票，可能预示着价格的快速上涨或下跌。
    3. 风险管理：收益率偏度可以作为风险指标，结合量价关系，有助于更全面地评估股票的风险。
    """
    # 1. 计算 ts_skewness(returns, 30)
    data_ts_skewness_returns = ts_skewness(data['returns'], 30)
    # 2. 计算 ts_delta(close, 10)
    data_ts_delta_close = ts_delta(data['close'], 10)
    # 3. 计算 ts_mean(vol, 60)
    data_ts_mean_vol = ts_mean(data['vol'], 60)
    # 4. 计算 divide(ts_delta(close, 10), ts_mean(vol, 60))
    data_divide = divide(data_ts_delta_close, data_ts_mean_vol)
    # 5. 计算 multiply(ts_skewness(returns, 30), divide(ts_delta(close, 10), ts_mean(vol, 60)))
    factor = multiply(data_ts_skewness_returns, data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()