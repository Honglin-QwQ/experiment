import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_sum, multiply

def factor_0014(data, **kwargs):
    """
    数学表达式: (-1 * ts_sum(rank(ts_corr(rank(high), rank(volume), 3)), 3))
    中文描述: 该因子计算了过去3天内，每天的成交量与最高价排名的相关性的时间序列之和的负数。具体来说，首先计算每天最高价和成交量各自的排名，然后计算这两个排名在过去3天内的相关性，接着对这个相关性进行排名，最后将过去3天排名的结果加总并取负数。这个因子可能反映了价格与成交量之间的关系，当价格和成交量的相关性越高，因子值越小，可能预示着价格反转的风险。
    应用场景：
    1. 可以作为反转策略的信号，当因子值较低时，买入股票。
    2. 可以与其他因子结合，构建更复杂的量化模型，例如，与动量因子结合，捕捉短期内的超卖反弹机会。
    3. 可以用于风险管理，当因子值持续较低时，降低仓位，规避潜在的下跌风险。
    """
    # 1. 计算 rank(high)
    data_rank_high = rank(data['high'])
    # 2. 计算 rank(volume)
    data_rank_volume = rank(data['vol'])
    # 3. 计算 ts_corr(rank(high), rank(volume), 3)
    data_ts_corr = ts_corr(data_rank_high, data_rank_volume, 3)
    # 4. 计算 rank(ts_corr(rank(high), rank(volume), 3))
    data_rank_ts_corr = rank(data_ts_corr)
    # 5. 计算 ts_sum(rank(ts_corr(rank(high), rank(volume), 3)), 3)
    data_ts_sum = ts_sum(data_rank_ts_corr, 3)
    # 6. 计算 -1 * ts_sum(rank(ts_corr(rank(high), rank(volume), 3)), 3)
    factor = multiply(-1, data_ts_sum)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()