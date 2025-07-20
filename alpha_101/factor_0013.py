import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delta, multiply

def factor_0013(data, **kwargs):
    """
    数学表达式: ((-1 * rank(ts_delta(returns, 3))) * ts_corr(open, volume, 10)) 
    中文描述: 描述：首先计算过去3天收益率的变化值，然后对这个变化值在所有股票中进行排序，数值越大排名越高，再取排名的负数。接着计算过去10天开盘价和成交量的相关性。最后，将负排名和相关性相乘，得到最终的因子值。这个因子试图捕捉收益变化趋势与量价关系之间的背离。
    应用场景：
    1. 可以用于构建量化选股策略，寻找收益下降但量价关系仍然紧密的股票，可能预示着反弹机会。
    2. 可以用于风险管理，识别收益下降且量价关系恶化的股票，可能预示着下跌风险。
    3. 可以结合其他因子，提高选股模型的准确性，例如，与价值因子、成长因子等结合使用。
    """
    # 1. 计算 ts_delta(returns, 3)
    delta_returns = ts_delta(data['returns'], 3)
    
    # 2. 计算 rank(ts_delta(returns, 3))
    ranked_delta_returns = rank(delta_returns, rate = 2)
    
    # 3. 计算 -1 * rank(ts_delta(returns, 3))
    negative_ranked_delta_returns = multiply(-1, ranked_delta_returns)
    
    # 4. 计算 ts_corr(open, volume, 10)
    correlation_open_volume = ts_corr(data['open'], data['vol'], 10)
    
    # 5. 计算 (-1 * rank(ts_delta(returns, 3))) * ts_corr(open, volume, 10)
    factor = multiply(negative_ranked_delta_returns, correlation_open_volume)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()