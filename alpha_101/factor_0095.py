import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_max, ts_rank, ts_decay_linear, ts_corr, rank, ts_arg_max, multiply,max

def factor_0095(data, **kwargs):
    """
    数学表达式: (ts_max(ts_rank(ts_decay_linear(ts_corr(rank(vwap), rank(volume), 3.83878), 4.16783), 8.38151), ts_rank(ts_decay_linear(ts_arg_max(ts_corr(ts_rank(close, 7.45404), ts_rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143)) * -1)
    中文描述: 该因子计算的是一个基于量价关系和时间衰减的综合指标，首先计算成交量加权平均价(vwap)和成交量的排序，并计算它们过去3.84天的相关性，然后对相关性进行4.17天的线性衰减，再计算过去8.38天衰减相关性的排序最大值；同时，计算收盘价和过去60天平均成交额(adv60)的排序，计算它们过去3.65天的相关性，找到过去12.66天相关性最大值出现的时间位置，然后对该位置进行14.04天的线性衰减，再计算过去13.41天衰减位置的排序；最后，取两个排序的最大值，并取负数。该因子可能捕捉量价关系的变化趋势和反转信号，可以应用于趋势跟踪、反转交易或高频交易策略中，例如，当因子值较高时，可能预示着价格下跌的风险，可以考虑卖出；当因子值较低时，可能预示着价格上涨的机会，可以考虑买入；或者结合其他技术指标，用于识别超买超卖区域。
    因子应用场景：
    1. 趋势跟踪：该因子可以用于识别股票价格的趋势，并据此进行买入或卖出操作。
    2. 反转交易：当因子值达到极端水平时，可能预示着价格即将反转，可以进行反向操作。
    3. 高频交易：该因子可以用于捕捉短期的量价关系变化，并进行高频交易。
    """
    # 1. 计算 rank(vwap)
    rank_vwap = rank(data['vwap'])
    # 2. 计算 rank(volume)
    rank_volume = rank(data['vol'])
    # 3. 计算 ts_corr(rank(vwap), rank(volume), 3.83878)
    ts_corr_rank_vwap_rank_volume = ts_corr(rank_vwap, rank_volume, 3.83878)
    # 4. 计算 ts_decay_linear(ts_corr(rank(vwap), rank(volume), 3.83878), 4.16783)
    ts_decay_linear_ts_corr_rank_vwap_rank_volume = ts_decay_linear(ts_corr_rank_vwap_rank_volume, 4.16783)
    # 5. 计算 ts_rank(ts_decay_linear(ts_corr(rank(vwap), rank(volume), 3.83878), 4.16783), 8.38151)
    ts_rank_ts_decay_linear_ts_corr_rank_vwap_rank_volume = ts_rank(ts_decay_linear_ts_corr_rank_vwap_rank_volume, 8.38151)
    # 6. 计算 ts_rank(close, 7.45404)
    ts_rank_close = ts_rank(data['close'], 7.45404)
    # 7. 计算 ts_rank(adv60, 4.13242)
    ts_rank_adv60 = ts_rank(data['amount'], 4.13242)
    # 8. 计算 ts_corr(ts_rank(close, 7.45404), ts_rank(adv60, 4.13242), 3.65459)
    ts_corr_ts_rank_close_ts_rank_adv60 = ts_corr(ts_rank_close, ts_rank_adv60, 3.65459)
    # 9. 计算 ts_arg_max(ts_corr(ts_rank(close, 7.45404), ts_rank(adv60, 4.13242), 3.65459), 12.6556)
    ts_arg_max_ts_corr_ts_rank_close_ts_rank_adv60 = ts_arg_max(ts_corr_ts_rank_close_ts_rank_adv60, 12.6556)
    # 10. 计算 ts_decay_linear(ts_arg_max(ts_corr(ts_rank(close, 7.45404), ts_rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365)
    ts_decay_linear_ts_arg_max_ts_corr_ts_rank_close_ts_rank_adv60 = ts_decay_linear(ts_arg_max_ts_corr_ts_rank_close_ts_rank_adv60, 14.0365)
    # 11. 计算 ts_rank(ts_decay_linear(ts_arg_max(ts_corr(ts_rank(close, 7.45404), ts_rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143)
    ts_rank_ts_decay_linear_ts_arg_max_ts_corr_ts_rank_close_ts_rank_adv60 = ts_rank(ts_decay_linear_ts_arg_max_ts_corr_ts_rank_close_ts_rank_adv60, 13.4143)
    # 12. 计算 ts_max(ts_rank(ts_decay_linear(ts_corr(rank(vwap), rank(volume), 3.83878), 4.16783), 8.38151), ts_rank(ts_decay_linear(ts_arg_max(ts_corr(ts_rank(close, 7.45404), ts_rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143))
    ts_max_ts_rank_decay_linear_corr_rank_ts_rank_decay_linear_argmax_corr = max(ts_rank_ts_decay_linear_ts_corr_rank_vwap_rank_volume, ts_rank_ts_decay_linear_ts_arg_max_ts_corr_ts_rank_close_ts_rank_adv60)
    # 13. 计算 (ts_max(ts_rank(ts_decay_linear(ts_corr(rank(vwap), rank(volume), 3.83878), 4.16783), 8.38151), ts_rank(ts_decay_linear(ts_arg_max(ts_corr(ts_rank(close, 7.45404), ts_rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143)) * -1)
    factor = multiply(ts_max_ts_rank_decay_linear_corr_rank_ts_rank_decay_linear_argmax_corr, -1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()