import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, multiply

def factor_0002(data, **kwargs):
    """
    数学表达式: (-1 * ts_corr(rank(open), rank(volume), 10))
    中文描述: 该因子计算过去10天内，每日开盘价排名与成交量排名之间的相关系数，并取负值。开盘价排名反映了市场对股票当日开盘的关注度，成交量排名反映了股票的交易活跃程度，二者相关性越高，说明市场对开盘价的预期与实际交易行为越一致。取负值后，因子值越高，表示开盘价排名与成交量排名之间的负相关性越强，即市场对开盘价的预期与实际交易行为越不一致。
    应用场景：
    1. 短期反转策略：因子值较高时，可能意味着市场情绪过度乐观或悲观，股价可能出现反转。
    2. 识别异常交易行为：因子值异常升高，可能表明存在操纵市场或内幕交易等行为。
    3. 量化选股：结合其他基本面或技术面因子，筛选出具有较高负相关性的股票，构建投资组合。
    """
    # 1. 计算 rank(open)
    data_rank_open = rank(data['open'])
    # 2. 计算 rank(volume)
    data_rank_volume = rank(data['vol'])
    # 3. 计算 ts_corr(rank(open), rank(volume), 10)
    data_ts_corr = ts_corr(data_rank_open, data_rank_volume, 10)
    # 4. 计算 -1 * ts_corr(rank(open), rank(volume), 10)
    factor = multiply(-1, data_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()