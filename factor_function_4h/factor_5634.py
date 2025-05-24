import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import floor, ts_corr, rank, ts_mean

def factor_5634(data, **kwargs):
    """
    因子名称: floor_open_vol_corr_rank_diff_76178
    数学表达式: rank(ts_corr(floor(open), vol, 5)) - rank(ts_mean(floor(open),5))
    中文描述: 该因子计算开盘价向下取整后与成交量的短期相关性排名，减去开盘价向下取整后的均值的排名。该因子旨在捕捉开盘价和成交量之间的关系，并将其与开盘价本身的变动趋势进行比较。创新点在于结合了floor(open)的离散化特性，使得因子对价格的微小波动不敏感，更关注价格的整体趋势。通过计算相关性和均值，并进行排名，可以更好地识别价格和成交量之间的关系。
    因子应用场景：
    1. 量价关系分析：用于识别开盘价和成交量之间存在异常关系的股票。
    2. 趋势验证：结合开盘价均值排名，验证成交量与价格趋势的一致性。
    """
    # 1. 计算 floor(open)
    data_floor_open = floor(data['open'])
    # 2. 计算 ts_corr(floor(open), vol, 5)
    data_ts_corr = ts_corr(data_floor_open, data['vol'], 5)
    # 3. 计算 rank(ts_corr(floor(open), vol, 5))
    rank_corr = rank(data_ts_corr, 2)
    # 4. 计算 ts_mean(floor(open), 5)
    data_ts_mean = ts_mean(data_floor_open, 5)
    # 5. 计算 rank(ts_mean(floor(open),5))
    rank_mean = rank(data_ts_mean, 2)
    # 6. 计算 rank(ts_corr(floor(open), vol, 5)) - rank(ts_mean(floor(open),5))
    factor = rank_corr - rank_mean

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()