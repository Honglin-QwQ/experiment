import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, subtract, ts_delta, ts_corr, rank, ts_std_dev
import pandas as pd

def factor_6071(data, **kwargs):
    """
    因子名称: TS_Delta_Corr_Vol_Std_Diff_Rank_Scaled_88634
    数学表达式: scale(subtract(ts_delta(ts_corr(high, vol, 10), 5), rank(ts_std_dev(close, 30))))
    中文描述: 该因子计算了过去5天内，过去10天最高价与成交量相关性的变化值，然后减去过去30天收盘价标准差的横截面排名，最后对结果进行缩放。
           该因子结合了量价关系的短期变化、价格波动的长期稳定性以及横截面排名信息，并通过减法操作和缩放引入了新的计算逻辑。
           相较于参考因子，该因子调整了相关性和标准差的窗口期，并使用减法代替除法，同时引入了缩放操作。
           这可能用于识别那些量价关系发生显著变化，并且相对于其他股票而言，其长期价格波动性较低的股票，同时通过缩放控制因子值的范围。
    因子应用场景：
    1. 量价关系分析：识别量价关系发生显著变化的股票。
    2. 波动性分析：结合长期价格波动性较低的股票。
    3. 风险控制：通过缩放控制因子值的范围，便于风险管理。
    """
    # 1. 计算 ts_corr(high, vol, 10)
    data_ts_corr = ts_corr(data['high'], data['vol'], 10)
    # 2. 计算 ts_delta(ts_corr(high, vol, 10), 5)
    data_ts_delta = ts_delta(data_ts_corr, 5)
    # 3. 计算 ts_std_dev(close, 30)
    data_ts_std_dev = ts_std_dev(data['close'], 30)
    # 4. 计算 rank(ts_std_dev(close, 30))
    data_rank = rank(data_ts_std_dev, 2)
    # 5. 计算 subtract(ts_delta(ts_corr(high, vol, 10), 5), rank(ts_std_dev(close, 30)))
    data_subtract = subtract(data_ts_delta, data_rank)
    # 6. 计算 scale(subtract(ts_delta(ts_corr(high, vol, 10), 5), rank(ts_std_dev(close, 30))))
    factor = scale(data_subtract)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()