import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_co_skewness, ts_rank, ts_corr, ts_std_dev, ts_mean, divide

def factor_6058(data, **kwargs):
    """
    因子名称: VolSkewPriceMomentum_90440
    数学表达式: rank(ts_co_skewness(vol, close, 10)) * ts_rank(ts_corr(ts_std_dev(high, 5), low, 5), 10) - ts_mean(divide(tbase, tquote), 15)
    中文描述: 该因子旨在捕捉成交量与价格的同步异动、价格波动与最低价的关联以及主动买卖力量的平衡。首先，计算过去10天内成交量与收盘价的协偏度并进行横截面排名，以识别成交量和价格倾向于同向大幅波动的股票。其次，计算过去5天内最高价标准差与最低价的相关性，并在过去10天内进行时间序列排名，衡量价格波动与最低价的动态关联强度。最后，计算过去15天内主动买入基础币种数量与主动买入计价币种数量比值的平均值，反映市场主动买卖力量的平衡。最终因子为前两部分的乘积减去主动买卖力量比值的平均值。创新点在于结合了成交量与收盘价的协偏度、高低价波动与最低价的时序相关性排名，并引入了主动买卖力量比值，从多个角度衡量市场的交易特征和趋势的潜在可持续性。
    因子应用场景：
    1. 市场情绪分析：该因子可用于识别市场中成交量和价格同步异动的股票，从而辅助判断市场情绪。
    2. 趋势跟踪：通过衡量价格波动与最低价的动态关联强度，该因子有助于捕捉趋势的潜在可持续性。
    3. 主动买卖力量平衡：该因子通过计算主动买卖力量比值的平均值，可以反映市场主动买卖力量的平衡状态。
    """
    # 1. 计算 ts_co_skewness(vol, close, 10)
    data_ts_co_skewness = ts_co_skewness(data['vol'], data['close'], 10)
    # 2. 计算 rank(ts_co_skewness(vol, close, 10))
    data_rank_ts_co_skewness = rank(data_ts_co_skewness, 2)
    # 3. 计算 ts_std_dev(high, 5)
    data_ts_std_dev = ts_std_dev(data['high'], 5)
    # 4. 计算 ts_corr(ts_std_dev(high, 5), low, 5)
    data_ts_corr = ts_corr(data_ts_std_dev, data['low'], 5)
    # 5. 计算 ts_rank(ts_corr(ts_std_dev(high, 5), low, 5), 10)
    data_ts_rank = ts_rank(data_ts_corr, 10)
    # 6. 计算 rank(ts_co_skewness(vol, close, 10)) * ts_rank(ts_corr(ts_std_dev(high, 5), low, 5), 10)
    factor_part1 = data_rank_ts_co_skewness * data_ts_rank
    # 7. 计算 divide(tbase, tquote)
    data_divide = divide(data['tbase'], data['tquote'])
    # 8. 计算 ts_mean(divide(tbase, tquote), 15)
    data_ts_mean = ts_mean(data_divide, 15)
    # 9. 计算 rank(ts_co_skewness(vol, close, 10)) * ts_rank(ts_corr(ts_std_dev(high, 5), low, 5), 10) - ts_mean(divide(tbase, tquote), 15)
    factor = factor_part1 - data_ts_mean

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()