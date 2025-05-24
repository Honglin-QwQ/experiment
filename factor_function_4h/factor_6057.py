import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import abs, ts_delta, ts_corr, rank, ts_std_dev, divide

def factor_6057(data, **kwargs):
    """
    因子名称: TS_Delta_Corr_Std_Rank_Ratio_41710
    数学表达式: divide(abs(ts_delta(ts_corr(high, vol, 5), 5)), rank(ts_std_dev(close, 20)))
    中文描述: 该因子计算了过去5天内，过去5天最高价与成交量相关性的绝对变化值，然后除以过去20天收盘价标准差的横截面排名。该因子创新性地结合了量价关系的短期变化、价格波动的长期稳定性以及横截面排名信息。通过计算相关性变化的绝对值，因子捕捉了量价关系的方向性突变；除以标准差的排名，则引入了横截面的比较信息，并对波动性进行了相对衡量。该因子可能用于识别那些量价关系发生显著变化，并且相对于其他股票而言，其长期价格波动性相对较低的股票，可能预示着潜在的交易机会。
    因子应用场景：
    1. 量价关系突变识别： 捕捉量价关系短期内的显著变化，可能预示着市场情绪或趋势的转变。
    2. 波动性比较： 结合长期价格波动性的横截面排名，筛选出量价关系变化明显但价格相对稳定的股票。
    3. 潜在交易机会： 识别出量价关系发生显著变化，且长期价格波动性相对较低的股票，可能预示着潜在的交易机会。
    """
    # 1. 计算 ts_corr(high, vol, 5)
    data_ts_corr = ts_corr(data['high'], data['vol'], 5)
    # 2. 计算 ts_delta(ts_corr(high, vol, 5), 5)
    data_ts_delta = ts_delta(data_ts_corr, 5)
    # 3. 计算 abs(ts_delta(ts_corr(high, vol, 5), 5))
    data_abs_ts_delta = abs(data_ts_delta)
    # 4. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 5. 计算 rank(ts_std_dev(close, 20))
    data_rank_ts_std_dev = rank(data_ts_std_dev, 2)
    # 6. 计算 divide(abs(ts_delta(ts_corr(high, vol, 5), 5)), rank(ts_std_dev(close, 20)))
    factor = divide(data_abs_ts_delta, data_rank_ts_std_dev)

    del data_ts_corr
    del data_ts_delta
    del data_abs_ts_delta
    del data_ts_std_dev
    del data_rank_ts_std_dev

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()