import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_min, ts_max, multiply

def factor_0054(data, **kwargs):
    """
    数学表达式: (-1 * ts_corr(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12)))), rank(volume), 6))
    中文描述: 该因子计算过去6天内，每天的收盘价减去过去12天最低价再除以过去12天最高价减去过去12天最低价的结果的排名，与成交量的排名的相关系数的负值，表达了价格相对位置与成交量之间的关系，负相关表示价格创新高时成交量反而萎缩，可能预示着反转，可以用于识别超买超卖现象，构建反转策略，或者作为其他量化模型的输入特征。
    因子应用场景：
    1. 反转策略：当因子值为负且绝对值较大时，可能预示着价格即将反转。
    2. 超买超卖识别：用于识别市场的超买超卖现象。
    3. 量化模型输入：作为其他量化模型的输入特征，提高模型的预测能力。
    """
    # 1. 计算 ts_min(low, 12)
    data_ts_min_low = ts_min(data['low'], d=12)
    # 2. 计算 ts_max(high, 12)
    data_ts_max_high = ts_max(data['high'], d=12)
    # 3. 计算 (ts_max(high, 12) - ts_min(low, 12))
    data_diff = (data_ts_max_high - data_ts_min_low)
    # 4. 计算 (close - ts_min(low, 12))
    data_close_min = (data['close'] - data_ts_min_low)
    # 5. 计算 ((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12)))
    data_normalized = data_close_min / data_diff
    # 6. 计算 rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12))))
    data_rank_price = rank(data_normalized)
    # 7. 计算 rank(volume)
    data_rank_volume = rank(data['vol'])
    # 8. 计算 ts_corr(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12)))), rank(volume), 6)
    data_ts_corr = ts_corr(data_rank_price, data_rank_volume, d=6)
    # 9. 计算 -1 * ts_corr(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12)))), rank(volume), 6)
    factor = multiply(-1, data_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()