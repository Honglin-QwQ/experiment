import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_covariance, multiply

def factor_0015(data, **kwargs):
    """
    数学表达式: (-1 * rank(ts_covariance(rank(high), rank(volume), 5)))
    中文描述: 这个因子计算了过去5天内，每天的成交量和最高价排名的协方差，然后对这个协方差进行排序，最后取负。这意味着如果一只股票在过去5天内，每天的成交量排名和最高价排名呈现负相关关系，并且这种负相关性在所有股票中排名靠前，那么这个因子的值就越大。
    因子应用场景：
    1. 可以用于短线反转策略，寻找超卖反弹的机会。
    2. 可以结合其他量价因子，构建更稳健的量化模型。
    3. 可以用于识别异常交易行为，例如主力资金拉高出货。
    """
    # 1. 计算 rank(high)
    rank_high = rank(data['high'])
    # 2. 计算 rank(volume)
    rank_volume = rank(data['vol'])
    # 3. 计算 ts_covariance(rank(high), rank(volume), 5)
    ts_covariance_rank_high_rank_volume = ts_covariance(rank_high, rank_volume, 5)
    # 4. 计算 rank(ts_covariance(rank(high), rank(volume), 5))
    rank_ts_covariance = rank(ts_covariance_rank_high_rank_volume, 2)
    # 5. 计算 -1 * rank(ts_covariance(rank(high), rank(volume), 5))
    factor = multiply(-1, rank_ts_covariance, filter=False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()