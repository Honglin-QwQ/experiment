import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import if_else, ts_rank, subtract, ts_mean, ts_partial_corr, ts_std_dev, ts_delta

def factor_5944(data, **kwargs):
    """
    因子名称: Volatility_Rank_Momentum_Interaction_V2_46139
    数学表达式: if_else(ts_rank(close, 45) > 0.85, -(amplitude - ts_mean(amplitude, 45)), if_else(ts_rank(close, 45) < 0.15, -(ts_mean(amplitude, 45) - amplitude), ts_partial_corr(ts_std_dev(close, 20), ts_delta(close, 15), ts_mean(vol, 10), 10)))
    中文描述: 该因子在参考因子和历史输出的基础上进一步提升。它沿用了在收盘价排名处于极端位置时捕捉波动性与极端价格排名关系的逻辑，但进一步扩展了时间窗口至45天，并收紧了极端排名的阈值（最高或最低15%），以聚焦更强的极端信号。最核心的创新在于，当收盘价排名处于中间时，因子计算的是过去20天收盘价标准差与过去15天收盘价变化量（动量）在过去10天内，剔除过去10天平均成交量影响下的偏相关性。这引入了成交量作为控制变量，旨在更精确地衡量波动率与价格动量之间的纯粹关系，排除由成交量变化引起的共同变动。这种设计使得因子能够更细致地捕捉市场在非极端情况下的复杂动态，结合了更严格的极端情况波动性反转逻辑和中间情况下去除成交量影响的波动率-动量偏相关分析，从而提供更具区分度的交易信号。参数（45天、20天、15天、10天）经过调整，旨在平衡因子的响应速度和稳定性，并进一步优化其预测能力。因子名修改以反映其包含的波动性、排名、动量以及偏相关分析的复杂交互逻辑。
    因子应用场景：
    1. 波动性反转：在收盘价排名极端时，捕捉市场可能出现的波动性反转信号。
    2. 动量与波动率关系：分析非极端情况下，剔除成交量影响的波动率与价格动量之间的关系。
    3. 市场复杂动态：更细致地捕捉市场在非极端情况下的复杂动态。
    """
    # 1. 计算 amplitude
    amplitude = data['high'] - data['low']

    # 2. 计算 ts_rank(close, 45)
    ts_rank_close_45 = ts_rank(data['close'], d=45)

    # 3. 计算 ts_mean(amplitude, 45)
    ts_mean_amplitude_45 = ts_mean(amplitude, d=45)

    # 4. 计算 -(amplitude - ts_mean(amplitude, 45))
    extreme_high = -(amplitude - ts_mean_amplitude_45)

    # 5. 计算 -(ts_mean(amplitude, 45) - amplitude)
    extreme_low = -(ts_mean_amplitude_45 - amplitude)

    # 6. 计算 ts_std_dev(close, 20)
    ts_std_dev_close_20 = ts_std_dev(data['close'], d=20)

    # 7. 计算 ts_delta(close, 15)
    ts_delta_close_15 = ts_delta(data['close'], d=15)

    # 8. 计算 ts_mean(vol, 10)
    ts_mean_vol_10 = ts_mean(data['vol'], d=10)

    # 9. 计算 ts_partial_corr(ts_std_dev(close, 20), ts_delta(close, 15), ts_mean(vol, 10), 10)
    ts_partial_corr_result = ts_partial_corr(ts_std_dev_close_20, ts_delta_close_15, ts_mean_vol_10, d=10)

    # 10. 计算 if_else(ts_rank(close, 45) < 0.15, -(ts_mean(amplitude, 45) - amplitude), ts_partial_corr(ts_std_dev(close, 20), ts_delta(close, 15), ts_mean(vol, 10), 10))
    inner_if_else = if_else(ts_rank_close_45 < 0.15, extreme_low, ts_partial_corr_result)

    # 11. 计算 if_else(ts_rank(close, 45) > 0.85, -(amplitude - ts_mean(amplitude, 45)), if_else(ts_rank(close, 45) < 0.15, -(ts_mean(amplitude, 45) - amplitude), ts_partial_corr(ts_std_dev(close, 20), ts_delta(close, 15), ts_mean(vol, 10), 10)))
    factor = if_else(ts_rank_close_45 > 0.85, extreme_high, inner_if_else)

    # 删除中间变量
    del amplitude
    del ts_rank_close_45
    del ts_mean_amplitude_45
    del extreme_high
    del extreme_low
    del ts_std_dev_close_20
    del ts_delta_close_15
    del ts_mean_vol_10
    del ts_partial_corr_result
    del inner_if_else

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()