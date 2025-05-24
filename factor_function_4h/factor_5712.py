import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank
from operators import ts_weighted_decay
from operators import multiply
from operators import ts_delta

def factor_5712(data, **kwargs):
    """
    因子名称: Exponentially_Decayed_Volume_Weighted_Price_Change_Ranked_81821
    数学表达式: rank(ts_weighted_decay(multiply(ts_delta(close, 6), vol), k=0.9))
    中文描述: 该因子旨在捕捉近期价格变动与交易量的结合信号，并进行指数衰减加权和排名处理。它首先计算过去6天收盘价的变化（ts_delta(close, 6)），然后将这个价格变化与当前交易量（vol）相乘，得到一个考虑了交易活跃度的短期价格动量信号。接着，使用ts_weighted_decay运算符对这个信号进行指数衰减加权处理，其中k=0.9赋予近期数据更高的权重，使得因子更侧重于最近的市场行为。最后，使用rank运算符对加权衰减后的信号进行截面排名，将原始因子值转换为相对排名，从而降低异常值的影响并提高因子的鲁棒性。相较于参考因子，创新点在于：1. 缩短了ts_delta的时间窗口，以捕捉更短期的动量；2. 调整了ts_weighted_decay的衰减系数，更强调近期数据；3. 引入了rank操作符，提高了因子的鲁棒性。该因子可以用于识别那些在近期价格变动显著、伴随高交易量且在所有股票中排名靠前的股票，并期望这种趋势在短期内持续。
    因子应用场景：
    1. 短期动量捕捉：识别近期价格和交易量均显著增加的股票。
    2. 趋势跟踪：寻找在短期内表现出强劲上升趋势的股票。
    3. 交易活跃度筛选：筛选出交易活跃且价格变化显著的股票。
    """
    # 1. 计算 ts_delta(close, 6)
    data_ts_delta = ts_delta(data['close'], d=6)
    # 2. 计算 multiply(ts_delta(close, 6), vol)
    data_multiply = multiply(data_ts_delta, data['vol'])
    # 3. 计算 ts_weighted_decay(multiply(ts_delta(close, 6), vol), k=0.9)
    data_ts_weighted_decay = ts_weighted_decay(data_multiply, k=0.9)
    # 4. 计算 rank(ts_weighted_decay(multiply(ts_delta(close, 6), vol), k=0.9))
    factor = rank(data_ts_weighted_decay)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()