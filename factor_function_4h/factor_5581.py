import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, multiply, ts_rank, ts_delta, log, divide, ts_delay

def factor_5581(data, **kwargs):
    """
    因子名称: factor_0002_61979
    数学表达式: ts_zscore(multiply(ts_rank(ts_delta(close, d=1), d=5), log(divide(high, ts_delay(low, d=1)))), d=20)
    中文描述: 该因子是对历史因子'ts_zscore(multiply(ts_rank(close, d=5), log(divide(high, low))), d=20)'的改进。它通过引入ts_delta(close, d=1)来捕捉收盘价的短期变化趋势，并使用ts_delay(low, d=1)来引入前一日的最低价作为参考，从而更精确地衡量日内价格波动。该因子旨在捕捉价格动量和波动率的结合，通过Z-score标准化，使其更具可比性。创新点在于使用收盘价差分和滞后最低价，增强了对短期价格变化的敏感性。
    因子应用场景：
    1. 动量捕捉：捕捉价格的短期变化趋势，对动量策略有较好的指示作用。
    2. 波动率衡量：通过比较当日最高价与前一日最低价，衡量日内价格波动。
    3. 趋势跟踪：结合动量和波动率，辅助判断市场趋势。
    """
    # 1. 计算 ts_delta(close, d=1)
    data_ts_delta = ts_delta(data['close'], d=1)
    # 2. 计算 ts_rank(ts_delta(close, d=1), d=5)
    data_ts_rank = ts_rank(data_ts_delta, d=5)
    # 3. 计算 ts_delay(low, d=1)
    data_ts_delay = ts_delay(data['low'], d=1)
    # 4. 计算 divide(high, ts_delay(low, d=1))
    data_divide = divide(data['high'], data_ts_delay)
    # 5. 计算 log(divide(high, ts_delay(low, d=1)))
    data_log = log(data_divide)
    # 6. 计算 multiply(ts_rank(ts_delta(close, d=1), d=5), log(divide(high, ts_delay(low, d=1))))
    data_multiply = multiply(data_ts_rank, data_log)
    # 7. 计算 ts_zscore(multiply(ts_rank(ts_delta(close, d=1), d=5), log(divide(high, ts_delay(low, d=1)))), d=20)
    factor = ts_zscore(data_multiply, d=20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()