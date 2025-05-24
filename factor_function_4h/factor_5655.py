import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, rank, ts_std_dev, multiply, divide, ts_sum

def factor_5655(data, **kwargs):
    """
    因子名称: volume_weighted_return_volatility_rank_decay_29489
    数学表达式: ts_decay_linear(rank(ts_std_dev(multiply(returns, divide(vol, ts_sum(vol, 20))), 20)), 10)
    中文描述: 该因子衡量的是成交量加权收益率波动率排名的线性衰减。首先计算每日收益率，然后用每日成交量进行加权，再计算过去20天加权收益率的标准差，并对该标准差进行横截面排名，最后计算过去10天该排名的线性衰减值。创新点在于，首先对波动率进行排名，降低了异常值的影响，使得因子对普遍的市场波动更为敏感。其次，引入线性衰减，使得最近的波动率排名变化对因子值的影响更大，能更敏感地反映市场参与度对价格波动的影响。适用于捕捉成交量活跃的股票的短期异常波动。
    因子应用场景：
    1. 捕捉成交量活跃的股票的短期异常波动。
    2. 识别市场参与度对价格波动的影响。
    """
    # 1. 计算 ts_sum(vol, 20)
    data_ts_sum_vol = ts_sum(data['vol'], 20)
    # 2. 计算 divide(vol, ts_sum(vol, 20))
    data_divide = divide(data['vol'], data_ts_sum_vol)
    # 3. 计算 multiply(returns, divide(vol, ts_sum(vol, 20)))
    data_multiply = multiply(data['returns'], data_divide)
    # 4. 计算 ts_std_dev(multiply(returns, divide(vol, ts_sum(vol, 20))), 20)
    data_ts_std_dev = ts_std_dev(data_multiply, 20)
    # 5. 计算 rank(ts_std_dev(multiply(returns, divide(vol, ts_sum(vol, 20))), 20))
    data_rank = rank(data_ts_std_dev, 2)
    # 6. 计算 ts_decay_linear(rank(ts_std_dev(multiply(returns, divide(vol, ts_sum(vol, 20))), 20)), 10)
    factor = ts_decay_linear(data_rank, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()