import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_rank, ts_std_dev, multiply, ts_zscore

def factor_5653(data, **kwargs):
    """
    因子名称: VolatilityAdjustedPriceMomentum_81101
    数学表达式: rank(ts_corr(high, vwap, 5)) + ts_rank(ts_std_dev(open, 15), 10) + multiply(low, ts_zscore(low, 2), filter = True)
    中文描述: 本因子融合了价格动量、波动率和低价超卖信号。它首先计算高价与成交量加权平均价（VWAP）的5日相关性的排名，捕捉市场情绪。然后，加上开盘价15日标准差的10日排名，衡量波动性。最后，乘以低价与其2日Z-score的乘积，识别短期超卖机会。该因子旨在综合考虑市场情绪、波动性和潜在的反转信号，为投资者提供更全面的决策依据。创新点在于将多个不同类型的因子信号进行有效结合，提升了因子在复杂市场环境下的适应性。
    因子应用场景：
    1. 市场情绪捕捉：通过高价与VWAP的相关性排名，反映市场对当前价格趋势的认可度。
    2. 波动率衡量：开盘价标准差的排名，评估市场的波动程度。
    3. 超卖机会识别：低价与Z-score的结合，寻找被低估的股票。
    """
    # 1. 计算 ts_corr(high, vwap, 5)
    data_ts_corr = ts_corr(data['high'], data['vwap'], 5)
    # 2. 计算 rank(ts_corr(high, vwap, 5))
    data_rank = rank(data_ts_corr, 2)
    # 3. 计算 ts_std_dev(open, 15)
    data_ts_std_dev = ts_std_dev(data['open'], 15)
    # 4. 计算 ts_rank(ts_std_dev(open, 15), 10)
    data_ts_rank = ts_rank(data_ts_std_dev, 10)
    # 5. 计算 ts_zscore(low, 2)
    data_ts_zscore = ts_zscore(data['low'], 2)
    # 6. 计算 multiply(low, ts_zscore(low, 2), filter = True)
    data_multiply = multiply(data['low'], data_ts_zscore, filter = True)
    # 7. 计算 rank(ts_corr(high, vwap, 5)) + ts_rank(ts_std_dev(open, 15), 10) + multiply(low, ts_zscore(low, 2), filter = True)
    factor = data_rank + data_ts_rank + data_multiply

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()