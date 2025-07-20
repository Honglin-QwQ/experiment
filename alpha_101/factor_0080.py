import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_sum, ts_product, log, multiply,adv

def factor_0080(data, **kwargs):
    """
    数学表达式: ((rank(Log(ts_product(rank((rank(ts_corr(vwap, ts_sum(adv10, 49.6054), 8.47743))^4)), 14.9655))) < rank(ts_corr(rank(vwap), rank(volume), 5.07914))) * -1) 
    中文描述: 1. 详细描述：该因子首先计算过去10天平均成交额adv10与49.6054之和，然后计算该和与当日成交额vwap在过去8.47743天的相关性，再将相关性结果取四次方，之后对四次方结果进行排序，并取排序结果的自然对数，最后计算该对数在过去14.9655天的乘积，并对乘积结果进行排序。同时，计算当日成交额vwap与成交量volume在过去5.07914天的相关性，并分别对vwap和volume进行排序后再计算相关性，再对相关性结果进行排序。比较前者的排序结果是否小于后者的排序结果，如果小于则赋值为-1，否则为0。该因子试图捕捉量价关系中的非线性模式，通过成交额和成交量的相关性以及时间序列上的变化，来判断股票的强弱趋势。
    2. 因子应用场景：
        - 短期反转策略：当因子值为-1时，可能意味着股票短期内被低估，可以考虑买入；当因子值为0时，可能意味着股票短期内被高估，可以考虑卖出。
        - 量化选股：将该因子与其他因子结合，作为选股模型的一部分，选择因子值较低的股票构建投资组合。
        - 风险预警：监控因子值的变化，当因子值出现异常波动时，可能预示着市场风险的增加，需要调整仓位或采取其他风险管理措施。
    """
    # 计算 adv10
    adv10 = adv(data['vol'],10)
    data['adv10'] = adv10

    # 计算 ts_sum(adv10, 49.6054)
    ts_sum_adv10 = ts_sum(data['adv10'], d = 10)

    # 计算 ts_corr(vwap, ts_sum(adv10, 49.6054), 8.47743)
    ts_corr_vwap = ts_corr(data['vwap'], ts_sum_adv10, d = 8.47743)

    # 计算 (ts_corr(vwap, ts_sum(adv10, 49.6054), 8.47743))^4
    ts_corr_vwap_pow4 = ts_corr_vwap ** 4

    # 计算 rank((ts_corr(vwap, ts_sum(adv10, 49.6054), 8.47743))^4)
    rank_ts_corr_vwap_pow4 = rank(ts_corr_vwap_pow4)

    # 计算 Log(rank((ts_corr(vwap, ts_sum(adv10, 49.6054), 8.47743))^4))
    log_rank_ts_corr_vwap_pow4 = log(rank_ts_corr_vwap_pow4)

    # 计算 ts_product(rank((rank(ts_corr(vwap, ts_sum(adv10, 49.6054), 8.47743))^4)), 14.9655)
    ts_product_log_rank = ts_product(log_rank_ts_corr_vwap_pow4, d = 14.9655)

    # 计算 rank(Log(ts_product(rank((rank(ts_corr(vwap, ts_sum(adv10, 49.6054), 8.47743))^4)), 14.9655)))
    rank_ts_product_log_rank = rank(ts_product_log_rank)

    # 计算 rank(vwap)
    rank_vwap = rank(data['vwap'])

    # 计算 rank(volume)
    rank_volume = rank(data['vol'])

    # 计算 ts_corr(rank(vwap), rank(volume), 5.07914)
    ts_corr_rank_vwap_volume = ts_corr(rank_vwap, rank_volume, d = 5.07914)

    # 计算 rank(ts_corr(rank(vwap), rank(volume), 5.07914))
    rank_ts_corr_rank_vwap_volume = rank(ts_corr_rank_vwap_volume)

    # 计算 (rank(Log(ts_product(rank((rank(ts_corr(vwap, ts_sum(adv10, 49.6054), 8.47743))^4)), 14.9655))) < rank(ts_corr(rank(vwap), rank(volume), 5.07914)))
    condition = (rank_ts_product_log_rank < rank_ts_corr_rank_vwap_volume)

    # 计算 ((rank(Log(ts_product(rank((rank(ts_corr(vwap, ts_sum(adv10, 49.6054), 8.47743))^4)), 14.9655))) < rank(ts_corr(rank(vwap), rank(volume), 5.07914))) * -1)
    factor = condition.astype(int) * -1

    # 删除中间变量
    del data['adv10']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()