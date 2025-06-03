import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_sum, multiply, subtract

def factor_0055(data, **kwargs):
    """
    数学表达式: (0 - (1 * (rank((ts_sum(returns, 10) / ts_sum(ts_sum(returns, 2), 3))) * rank((returns * cap))))) 
    中文描述: 该因子首先计算过去10天收益率的总和，然后除以过去3天内，每天过去2天收益率总和的总和，并对结果进行排序；同时计算收益率与流通市值的乘积，并进行排序；将两个排序结果相乘，取负数。该因子可能捕捉了短期收益动量与市值效应的某种负相关关系，即过去一段时间收益率较高且市值较大的股票，未来收益率可能较低。
    应用场景：
    1. 构造反转策略，做空该因子值高的股票，做多该因子值低的股票。
    2. 作为风险因子，在多因子模型中控制市值和短期动量带来的风险敞口。
    3. 用于识别高估值的股票，因子值高的股票可能被认为是被高估的。
    """
    # 1. 计算 ts_sum(returns, 10)
    ts_sum_returns_10 = ts_sum(data['returns'], 10)
    
    # 2. 计算 ts_sum(returns, 2)
    ts_sum_returns_2 = ts_sum(data['returns'], 2)
    
    # 3. 计算 ts_sum(ts_sum(returns, 2), 3)
    ts_sum_ts_sum_returns_2_3 = ts_sum(ts_sum_returns_2, 3)
    
    # 4. 计算 (ts_sum(returns, 10) / ts_sum(ts_sum(returns, 2), 3))
    divide_result = ts_sum_returns_10 / ts_sum_ts_sum_returns_2_3
    
    # 5. 计算 rank((ts_sum(returns, 10) / ts_sum(ts_sum(returns, 2), 3)))
    rank_result_1 = rank(divide_result, 2)
    
    # 6. 计算 (returns * cap)
    returns_multiply_cap = multiply(data['returns'], data['total_mv'])
    
    # 7. 计算 rank((returns * cap))
    rank_result_2 = rank(returns_multiply_cap, 2)
    
    # 8. 计算 (rank((ts_sum(returns, 10) / ts_sum(ts_sum(returns, 2), 3))) * rank((returns * cap)))
    multiply_result = multiply(rank_result_1, rank_result_2)
    
    # 9. 计算 (0 - (1 * (rank((ts_sum(returns, 10) / ts_sum(ts_sum(returns, 2), 3))) * rank((returns * cap)))))
    factor = subtract(0, multiply(1, multiply_result))

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()