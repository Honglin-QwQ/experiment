import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_covariance, multiply

def factor_0012(data, **kwargs):
    """
    数学表达式: (-1 * rank(ts_covariance(rank(close), rank(volume), 5)))
    中文描述: 详细描述：这个因子首先计算了过去5天收盘价和成交量的排序，然后计算这两个排序之间的协方差，接着对协方差进行排序，最后取排序的负数。这个因子的含义是，如果过去5天收盘价和成交量的排序协方差越大，说明价格和成交量同向变动的趋势越明显，因子值就越小，反之亦然。取负号是为了反转这种关系，使得价格和成交量同向变动越明显，因子值越大。
    因子应用场景：
    1. 可以用于识别价格和成交量之间关系异常的股票，例如，价格上涨但成交量下降的股票，这些股票可能存在短期回调的机会。
    2. 可以用于构建量价组合策略，例如，买入因子值高的股票，卖出因子值低的股票。
    3. 可以作为其他因子的补充，例如，与其他技术指标或基本面因子结合使用，提高选股的准确性。
    """
    # 1. 计算 rank(close)
    data_rank_close = rank(data['close'])
    # 2. 计算 rank(volume)
    data_rank_volume = rank(data['vol'])
    # 3. 计算 ts_covariance(rank(close), rank(volume), 5)
    data_ts_covariance = ts_covariance(data_rank_close, data_rank_volume, 5)
    # 4. 计算 rank(ts_covariance(rank(close), rank(volume), 5))
    data_rank_ts_covariance = rank(data_ts_covariance)
    # 5. 计算 -1 * rank(ts_covariance(rank(close), rank(volume), 5))
    factor = multiply(-1, data_rank_ts_covariance)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()