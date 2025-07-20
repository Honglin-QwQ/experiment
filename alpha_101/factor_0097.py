import inspect
import numpy as np
from operators import ts_rank, ts_decay_linear, ts_corr, indneutralize, ts_std_dev, signed_power, divide, multiply, add

def factor_0097(data, **kwargs):
    """
    数学表达式: (-1 * ts_rank(ts_decay_linear(ts_corr(indneutralize(close, IndClass.sector), ts_decay_linear(volume, 5.0), 9.0), 8.0), 6.0)) + (ts_std_dev(vwap, 15) * signed_power(divide(open, close), 3) / ts_std_dev(returns, 10))
    中文描述: AlphaTrend_Volatility_Reversal是一个综合性的复合因子，旨在通过结合价格趋势、成交量行为和波动率信号来捕捉股票的潜在反转机会。该因子主要由两部分相加构成：
    1. 行业中性化情绪与交易健康度（借鉴factor_0057和factor_0090的优化）：
        *   首先通过indneutralize(close, IndClass.sector)对收盘价进行行业中性化处理，剥离行业因素对个股价格的影响，从而更清晰地关注股票自身的价格走势和相对表现。
        *   对成交量volume进行ts_decay_linear线性衰减处理，赋予近期成交量更大的权重，以更灵敏地反映当前的交易活跃度和资金流动情况。衰减周期设置为5天。
        *   计算经过行业中性化处理的收盘价与衰减后的成交量在过去9天内的ts_corr相关性。这衡量了股票价格变动与交易活跃度之间的同步性，反映了市场对该股票的关注程度和交易的“健康”状态。
        *   对这个相关性结果进行8天的ts_decay_linear线性衰减，进一步平滑并强调近期相关性的趋势。
        *   最后，计算衰减后相关性在过去6天的ts_rank时序排名，并乘以-1。取负值是为了捕捉反向逻辑：当价格与成交量协同性较弱（相关性较低），可能意味着市场关注度不足或存在错位定价，此时因子值较高，预示潜在的反转机会。

    2. 价格波动与日内力量对比（借鉴factor_0093和factor_0053的创新融合）：
        *   计算vwap（成交量加权平均价）在过去15天内ts_std_dev标准差，作为短期价格波动率的衡量。高波动率可能预示着趋势变化或反转的可能性。
        *   计算open开盘价与close收盘价的比值，并进行signed_power三次方处理，以放大日内开盘与收盘价之间的相对力量。这个比值直接反映了日内多空博弈的结果，如果开盘价远高于收盘价，可能预示日内卖压较强。
        *   计算returns在过去10天内ts_std_dev标准差，作为整体短期回报波动率的衡量。将其作为分母，通过与vwap波动率的比值，对日内力量和价格波动进行标准化，防止极端波动对因子产生过大的影响。
        *   将上述两个部分（vwap波动率项和日内力量项）相乘后，再除以回报波动率。这一部分旨在捕捉那些在近期价格波动剧烈且日内开盘/收盘价位差异较大的股票。当价格波动较大且日内表现出明确的方向性时，可能暗示着短期内的价格过度行为或反转信号。

    综合逻辑：
    AlphaTrend_Volatility_Reversal因子将上述两大部分进行加性组合。第一部分侧重于中长期维度上，股票在行业背景下的量价关系异象，寻找市场可能低估的股票。第二部分则专注于短期内，通过价格波动率和日内交易行为捕捉潜在的超买超卖或趋势耗尽。综合来看，该因子旨在识别那些在行业内表现出异常的价格-成交量关系，同时在短期内又出现了显著的价格波动和日内方向性变化的股票，这些特征通常与股票的重大趋势或反转点相关。

    应用场景：
    1.  趋势反转策略：因子值较高的股票可能具备较强的反转潜力，适合构建多头组合；因子值较低的股票则可能存在负向反转，可构建空头组合。
    2.  量化择时：结合价格和成交量信息，可以在宏观经济或市场情绪变化时，挑选出有望领先反转的股票。
    3.  多因子模型构建：作为核心因子加入多因子模型，与其他基本面、成长性或质量因子结合，提升模型的预测能力。
    4.  风险辅助指标：当因子值极端时，可能提示市场情绪或结构性异动，可作为辅助风险警示指标。
    """

    # Factor Part 1: Industry-Neutralized Price-Volume Relationship
    # 1. indneutralize(close, IndClass.sector)
    ind_neutralized_close = indneutralize(data['close'], data['industry'])

    # 2. ts_decay_linear(volume, 5.0)
    decayed_volume = ts_decay_linear(data['vol'], d=5.0)

    # 3. ts_corr(indneutralize(close, IndClass.sector), ts_decay_linear(volume, 5.0), 9.0)
    corr_price_volume = ts_corr(ind_neutralized_close, decayed_volume, d=9.0)

    # 4. ts_decay_linear(corr_price_volume, 8.0)
    decayed_corr = ts_decay_linear(corr_price_volume, d=8.0)

    # 5. ts_rank(decayed_corr, 6.0) * -1
    factor_part_1 = ts_rank(decayed_corr, d=6.0) * -1

    # Factor Part 2: Volatility and Intraday Power
    # 1. ts_std_dev(vwap, 15)
    vwap_std_dev = ts_std_dev(data['vwap'], d=15)

    # 2. divide(open, close)
    open_close_ratio = divide(data['open'], data['close'])

    # 3. signed_power(open_close_ratio, 3)
    intraday_power = signed_power(open_close_ratio, 3)

    # 4. ts_std_dev(returns, 10)
    returns_std_dev = ts_std_dev(data['returns'], d=10)

    # Handle division by zero for returns_std_dev
    returns_std_dev_safe = returns_std_dev.replace(0, np.nan) # Replace 0 with NaN to avoid division by zero

    # 5. (vwap_std_dev * intraday_power) / returns_std_dev
    # Ensure safe division, result will be NaN where returns_std_dev_safe is NaN
    intraday_vol_ratio = divide(multiply(vwap_std_dev, intraday_power), returns_std_dev_safe) # Using divide operator
    
    # Replace inf and -inf values with NaN if any produced by division
    # This is handled internally by some operators or might need explicit handling from numpy
    intraday_vol_ratio = intraday_vol_ratio.replace([np.inf, -np.inf], np.nan)

    # Combine the two parts
    factor = add(factor_part_1, intraday_vol_ratio)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()