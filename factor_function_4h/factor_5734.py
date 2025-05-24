import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, divide, ts_weighted_decay, multiply, ts_delta, log, ts_std_dev

def factor_5734(data, **kwargs):
    """
    数学表达式: rank(divide(ts_weighted_decay(multiply(ts_delta(close, 3), log(vol)), k=0.95), ts_std_dev(close, 10)))
    中文描述: 该因子旨在捕捉短期价格-交易量动量与长期价格波动率的比率，并进行指数衰减加权和排名处理。它首先计算过去3天收盘价的变化（ts_delta(close, 3)），并对交易量取对数（log(vol)）以降低量纲影响。然后将这两者相乘，得到一个考虑了交易活跃度的短期价格动量信号。接着，使用ts_weighted_decay运算符对这个信号进行指数衰减加权处理，其中k=0.95赋予近期数据更高的权重。同时，计算过去10天收盘价的标准差（ts_std_dev(close, 10)）作为长期价格波动率的衡量。最后，将加权衰减后的短期价格-交易量信号除以长期价格波动率，得到一个反映单位波动率下短期动量的比率，并使用rank运算符对这个比率进行截面排名。相较于参考因子，创新点在于：1. 缩短了ts_delta的时间窗口以捕捉更短期的动量；2. 对交易量进行了对数变换；3. 将短期动量信号与长期价格波动率的比值作为因子基础；4. 调整了ts_weighted_decay的衰减系数；5. 引入了rank操作符进行截面排名。该因子可以用于识别那些在近期价格变动显著、伴随高交易量，且相对于其长期波动率而言短期动量较强的股票，并期望这种相对强势在短期内持续。
    因子应用场景：
    1. 短期动量捕捉：识别短期内价格上涨且交易量活跃的股票。
    2. 波动率调整：衡量相对于长期波动率的短期动量强度。
    3. 相对强势识别：筛选在截面上表现出相对强势的股票。
    """
    # 1. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], d=3)
    # 2. 计算 log(vol)
    data_log_vol = log(data['vol'])
    # 3. 计算 multiply(ts_delta(close, 3), log(vol))
    data_multiply = multiply(data_ts_delta_close, data_log_vol)
    # 4. 计算 ts_weighted_decay(multiply(ts_delta(close, 3), log(vol)), k=0.95)
    data_ts_weighted_decay = ts_weighted_decay(data_multiply, k=0.95)
    # 5. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], d=10)
    # 6. 计算 divide(ts_weighted_decay(multiply(ts_delta(close, 3), log(vol)), k=0.95), ts_std_dev(close, 10))
    data_divide = divide(data_ts_weighted_decay, data_ts_std_dev_close)
    # 7. 计算 rank(divide(ts_weighted_decay(multiply(ts_delta(close, 3), log(vol)), k=0.95), ts_std_dev(close, 10)))
    factor = rank(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()