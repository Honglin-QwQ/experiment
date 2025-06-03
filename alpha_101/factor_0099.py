import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_scale, indneutralize, ts_corr, ts_arg_min, divide, multiply, subtract, adv

def factor_0099(data, **kwargs):
    """
    数学表达式: (0 - (1 * (((1.5 * ts_scale(indneutralize(indneutralize(rank(((((close - low) - (high - close)) / (high - low)) * volume)), IndClass.subindustry), IndClass.subindustry))) - ts_scale(indneutralize((ts_corr(close, rank(adv20), 5) - rank(ts_arg_min(close, 30))), IndClass.subindustry))) * (volume / adv20))))
    中文描述: 该因子首先计算一个基于成交量加权的日内价格波动指标，然后对其进行两次行业中性化和排序，并进行时间序列标准化；同时，计算收盘价与过去20日平均成交额排名的相关性，减去过去30日收盘价最低值出现的位置排名，进行行业中性化和时间序列标准化；将两个标准化后的结果相减，乘以成交量与过去20日平均成交额的比值，最后取负数。该因子可能捕捉了日内价格波动和成交量变化之间的关系，以及收盘价与成交量之间的相关性，并结合了行业中性化来消除行业偏差，可用于量化选股、构建多因子模型，或者作为高频交易中的一个信号。
    因子应用场景：
    1. 量化选股：该因子可以作为量化选股模型中的一个因子，用于衡量股票的日内价格波动和成交量变化之间的关系。
    2. 多因子模型：该因子可以与其他因子结合，构建多因子模型，提高选股的准确性。
    3. 高频交易：该因子可以作为高频交易中的一个信号，用于判断股票的短期走势。
    """
    # 计算adv20
    adv20 = adv(data['vol'],20)
    # 计算(((close - low) - (high - close)) / (high - low)) * volume
    inner_price_volatility = (((data['close'] - data['low']) - (data['high'] - data['close'])) / (data['high'] - data['low'])) * data['vol']
    # 对inner_price_volatility进行rank
    ranked_inner_price_volatility = rank(inner_price_volatility)
    # 对ranked_inner_price_volatility进行两次行业中性化
    indneutralized_ranked_inner_price_volatility_1 = indneutralize(ranked_inner_price_volatility, data['industry'])
    indneutralized_ranked_inner_price_volatility_2 = indneutralize(indneutralized_ranked_inner_price_volatility_1, data['industry'])
    # 对indneutralized_ranked_inner_price_volatility_2进行时间序列标准化
    ts_scaled_indneutralized_ranked_inner_price_volatility = ts_scale(indneutralized_ranked_inner_price_volatility_2)
    # 计算rank(adv20)
    ranked_adv20 = rank(adv20)
    # 计算ts_corr(close, rank(adv20), 5)
    corr_close_ranked_adv20 = ts_corr(data['close'], ranked_adv20, 5)
    # 计算ts_arg_min(close, 30)
    ts_arg_min_close_30 = ts_arg_min(data['close'], 30)
    # 计算rank(ts_arg_min(close, 30))
    ranked_ts_arg_min_close_30 = rank(ts_arg_min_close_30)
    # 计算ts_corr(close, rank(adv20), 5) - rank(ts_arg_min(close, 30))
    corr_minus_rank = subtract(corr_close_ranked_adv20, ranked_ts_arg_min_close_30)
    # 对corr_minus_rank进行行业中性化
    indneutralized_corr_minus_rank = indneutralize(corr_minus_rank, data['industry'])
    # 对indneutralized_corr_minus_rank进行时间序列标准化
    ts_scaled_indneutralized_corr_minus_rank = ts_scale(indneutralized_corr_minus_rank)
    # 计算ts_scaled_indneutralized_ranked_inner_price_volatility - ts_scaled_indneutralized_corr_minus_rank
    diff = subtract(ts_scaled_indneutralized_ranked_inner_price_volatility, ts_scaled_indneutralized_corr_minus_rank)
    # 计算volume / adv20
    volume_over_adv20 = divide(data['vol'], adv20)
    # 计算(ts_scaled_indneutralized_ranked_inner_price_volatility - ts_scaled_indneutralized_corr_minus_rank) * (volume / adv20)
    mult = multiply(diff, volume_over_adv20)
    # 计算0 - (1 * mult)
    factor = (0 - (1 * mult))

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()