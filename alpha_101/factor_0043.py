import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, multiply

def factor_0043(data, **kwargs):
    """
    数学表达式: (-1 * ts_corr(high, rank(volume), 5))
    中文描述: 描述：该因子首先计算过去5天内，每天的最高价和成交量排名的相关系数，成交量排名越高，则数值越大，然后将相关系数乘以-1。该因子衡量了价格上涨与成交量之间的关系，负相关表示价格上涨时成交量反而下降，可能预示着潜在的抛售压力或价格反转。
    因子应用场景：
    1. 识别潜在的超买股票：当因子值较高时，可能表明价格上涨并未得到成交量的支持，股票可能处于超买状态，存在回调风险。
    2. 短线反转策略：寻找因子值快速上升的股票，表明近期价格上涨与成交量之间的负相关性增强，可能预示着价格即将下跌，可以考虑做空。
    3. 结合其他因子：可以将该因子与其他量价因子结合使用，例如波动率、动量等，构建更稳健的量化交易模型。
    """
    # 1. 计算 rank(volume)
    data_rank_volume = rank(data['vol'])
    # 2. 计算 ts_corr(high, rank(volume), 5)
    data_ts_corr = ts_corr(data['high'], data_rank_volume, 5)
    # 3. 计算 -1 * ts_corr(high, rank(volume), 5)
    factor = multiply(-1, data_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()