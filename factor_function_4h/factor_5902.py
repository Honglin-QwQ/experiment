import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_rank, sigmoid, ts_delta, multiply

def factor_5902(data, **kwargs):
    """
    因子名称: ts_rank_sigmoid_delta_vwap_returns_52690
    数学表达式: ts_rank(sigmoid(ts_delta(vwap, 5)) * ts_delta(returns, 3), 120)
    中文描述: 该因子结合了VWAP的短期变化、收益率的短期变化以及Sigmoid函数的非线性特性，计算了一个综合指标在较长时间窗口内的排名。具体来说，它首先计算VWAP在过去5天的变化量并应用Sigmoid函数进行平滑和归一化，然后将这个结果与收益率在过去3天的变化量相乘。最后，计算这个乘积在过去120天内的排名。Sigmoid函数的使用引入了非线性，使得因子对VWAP变化的敏感度在高低值时有所不同。将经过Sigmoid处理的VWAP变化与收益率变化相乘，旨在捕捉价格和收益率变化的协同效应。在量化投资中，高排名可能表明近期市场情绪和价格/收益率变化在历史上的相对强势，可用于动量或反转策略。
    因子应用场景：
    1. 动量策略：高因子值可能表示近期市场情绪和价格/收益率变化在历史上的相对强势，可以作为买入信号。
    2. 反转策略：结合其他指标，低因子值可能预示着超卖状态，可以作为潜在的买入机会。
    """
    # 1. 计算 ts_delta(vwap, 5)
    data_ts_delta_vwap = ts_delta(data['vwap'], 5)
    # 2. 计算 sigmoid(ts_delta(vwap, 5))
    data_sigmoid = sigmoid(data_ts_delta_vwap)
    # 3. 计算 ts_delta(returns, 3)
    data_ts_delta_returns = ts_delta(data['returns'], 3)
    # 4. 计算 sigmoid(ts_delta(vwap, 5)) * ts_delta(returns, 3)
    data_multiply = multiply(data_sigmoid, data_ts_delta_returns)
    # 5. 计算 ts_rank(sigmoid(ts_delta(vwap, 5)) * ts_delta(returns, 3), 120)
    factor = ts_rank(data_multiply, 120)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()