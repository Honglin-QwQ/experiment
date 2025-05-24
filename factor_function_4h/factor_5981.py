import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_std_dev, ts_decay_linear, ts_returns, multiply, rank

def factor_5981(data, **kwargs):
    """
    数学表达式: rank(multiply(ts_delta(ts_std_dev(close, 10), 1), ts_decay_linear(ts_returns(close, 5), 5)))
    中文描述: 该因子结合了短期波动率的变化和短期收益的线性衰减平均值，并对结果进行排名。它计算了10天收盘价标准差的日变化，并将其与过去5天收盘价的线性衰减收益率相乘。当短期波动率增加（ts_delta(ts_std_dev(close, 10), 1) > 0）且短期收益为正（ts_decay_linear(ts_returns(close, 5), 5) > 0）时，因子值可能较高，表明波动率和价格都在上涨，可能预示着趋势的加速。反之，当波动率下降且收益为负时，因子值可能较低，预示着下跌趋势的延续或加速。
    因子应用场景：
    1. 趋势跟踪：识别波动率和价格同步变动的趋势信号。
    2. 动量策略：结合波动率变化捕捉动量加速或减速。
    3. 风险管理：监测因子极端值，识别潜在的市场风险或趋势反转信号。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 2. 计算 ts_delta(ts_std_dev(close, 10), 1)
    data_ts_delta = ts_delta(data_ts_std_dev, 1)
    # 3. 计算 ts_returns(close, 5)
    data_ts_returns = ts_returns(data['close'], 5)
    # 4. 计算 ts_decay_linear(ts_returns(close, 5), 5)
    data_ts_decay_linear = ts_decay_linear(data_ts_returns, 5)
    # 5. 计算 multiply(ts_delta(ts_std_dev(close, 10), 1), ts_decay_linear(ts_returns(close, 5), 5))
    data_multiply = multiply(data_ts_delta, data_ts_decay_linear)
    # 6. 计算 rank(multiply(ts_delta(ts_std_dev(close, 10), 1), ts_decay_linear(ts_returns(close, 5), 5)))
    factor = rank(data_multiply, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()