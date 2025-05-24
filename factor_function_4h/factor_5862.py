import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_skewness, multiply, ts_returns, ts_std_dev

def factor_5862(data, **kwargs):
    """
    因子名称: VolumeWeightedPriceVolatilitySkewnessRatio_89503
    数学表达式: divide(ts_skewness(multiply(ts_returns(close, 5), vol), 15), ts_skewness(vol, 15))
    中文描述: 该因子是基于历史输出和改进建议的创新。它计算过去15天内成交量加权收益率的偏度与过去15天成交量偏度的比值。与原始因子直接使用收盘价偏度不同，这里引入了成交量加权的收益率，更能体现大额交易对价格波动非对称性的影响。同时，使用收益率偏度而非价格偏度，消除了趋势的影响，更准确地反映价格变化的本质。该因子旨在捕捉市场微观结构对价格非对称波动的影响，特别是在成交量活跃时的价格偏离情况。高值可能表明在成交量放大的情况下，价格倾向于向一个方向剧烈波动，这可用于识别潜在的趋势反转或加速信号。
    因子应用场景：
    1. 识别潜在的趋势反转或加速信号。
    2. 捕捉市场微观结构对价格非对称波动的影响。
    """
    # 1. 计算 ts_returns(close, 5)
    data_ts_returns = ts_returns(data['close'], 5)
    # 2. 计算 multiply(ts_returns(close, 5), vol)
    data_multiply = multiply(data_ts_returns, data['vol'])
    # 3. 计算 ts_skewness(multiply(ts_returns(close, 5), vol), 15)
    data_ts_skewness_1 = ts_skewness(data_multiply, 15)
    # 4. 计算 ts_skewness(vol, 15)
    data_ts_skewness_2 = ts_skewness(data['vol'], 15)
    # 5. 计算 divide(ts_skewness(multiply(ts_returns(close, 5), vol), 15), ts_skewness(vol, 15))
    factor = divide(data_ts_skewness_1, data_ts_skewness_2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()