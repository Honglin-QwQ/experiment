import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_max, rank, ts_decay_linear, ts_delta, ts_rank, abs, ts_corr, multiply, subtract,indneutralize,adv

def factor_0086(data, **kwargs):
    """
    数学表达式: (ts_max(rank(ts_decay_linear(ts_delta(((close * 0.369701) + (vwap * (1 - 0.369701))), 1.91233), 2.65461)), ts_rank(ts_decay_linear(abs(ts_corr(indneutralize(adv81, IndClass.industry), close, 13.4132)), 4.89768), 14.4535)) * -1)
    中文描述: 该因子计算的是一个综合排序指标，首先计算收盘价乘以0.369701加上成交额加权平均价乘以(1-0.369701)的加权价格，然后计算该加权价格的1.91233日差分，再对差分结果进行2.65461日线性衰减加权，并计算衰减加权值的排序，取过去一段时间（由ts_max决定）内的最大值；同时，计算过去13.4132日行业中性化的成交额均值与收盘价的相关性的绝对值的4.89768日线性衰减加权，再计算衰减加权值的排序，取过去一段时间（由ts_max决定）内的排名；最后，将两个排序结果相乘并取负值。该因子的金融意义在于捕捉价格和成交量变化趋势的加速或减速，并结合成交额与价格相关性的变化，寻找市场反转或者趋势延续的机会。应用场景包括：1. 短线反转策略：当因子值较大时，可能预示着超跌反弹的机会。2. 趋势跟踪策略：结合其他趋势指标，当因子值持续下降时，可能确认上升趋势。3. 量价关系分析：该因子可以作为量价关系研究的输入特征，用于预测股票收益。
    """
    # 1. 计算 ((close * 0.369701) + (vwap * (1 - 0.369701)))
    data['weighted_price'] = data['close'] * 0.369701 + data['vwap'] * (1 - 0.369701)

    # 2. 计算 ts_delta(((close * 0.369701) + (vwap * (1 - 0.369701))), 1.91233)
    data['delta_weighted_price'] = ts_delta(data['weighted_price'], d = 1.91233)

    # 3. 计算 ts_decay_linear(ts_delta(((close * 0.369701) + (vwap * (1 - 0.369701))), 1.91233), 2.65461)
    data['decay_delta_weighted_price'] = ts_decay_linear(data['delta_weighted_price'], d = 2.65461)

    # 4. 计算 rank(ts_decay_linear(ts_delta(((close * 0.369701) + (vwap * (1 - 0.369701))), 1.91233), 2.65461))
    data['rank_decay_delta_weighted_price'] = rank(data['decay_delta_weighted_price'])

    # 5. 计算 adv81
    data['adv81'] = adv(data['vol'],81)

    # 6. 计算 indneutralize(adv81, IndClass.industry)
    data['neutralized_adv81'] = indneutralize(data['adv81'], data['industry'])

    # 7. 计算 ts_corr(indneutralize(adv81, IndClass.industry), close, 13.4132)
    data['corr_adv_close'] = ts_corr(data['neutralized_adv81'], data['close'], d = 13.4132)

    # 8. 计算 abs(ts_corr(indneutralize(adv81, IndClass.industry), close, 13.4132))
    data['abs_corr_adv_close'] = abs(data['corr_adv_close'])

    # 9. 计算 ts_decay_linear(abs(ts_corr(indneutralize(adv81, IndClass.industry), close, 13.4132)), 4.89768)
    data['decay_abs_corr_adv_close'] = ts_decay_linear(data['abs_corr_adv_close'], d = 4.89768)

    # 10. 计算 ts_rank(ts_decay_linear(abs(ts_corr(indneutralize(adv81, IndClass.industry), close, 13.4132)), 4.89768), 14.4535)
    data['rank_decay_abs_corr_adv_close'] = ts_rank(data['decay_abs_corr_adv_close'], d = 14.4535)

    # 11. 计算 ts_max(rank(ts_decay_linear(ts_delta(((close * 0.369701) + (vwap * (1 - 0.369701))), 1.91233), 2.65461)), ts_rank(ts_decay_linear(abs(ts_corr(indneutralize(adv81, IndClass.industry), close, 13.4132)), 4.89768), 14.4535))
    data['max_rank'] = ts_max(data['rank_decay_delta_weighted_price'], d = 10)
    factor = multiply(data['max_rank'], data['rank_decay_abs_corr_adv_close'], filter=False)

    # 12. 计算 (ts_max(rank(ts_decay_linear(ts_delta(((close * 0.369701) + (vwap * (1 - 0.369701))), 1.91233), 2.65461)), ts_rank(ts_decay_linear(abs(ts_corr(indneutralize(adv81, IndClass.industry), close, 13.4132)), 4.89768), 14.4535)) * -1)
    factor = multiply(factor, -1, filter=False)

    data.drop(columns=['weighted_price', 'delta_weighted_price', 'decay_delta_weighted_price', 'rank_decay_delta_weighted_price', 'adv81', 'neutralized_adv81', 'corr_adv_close', 'abs_corr_adv_close', 'decay_abs_corr_adv_close', 'rank_decay_abs_corr_adv_close', 'max_rank'], inplace=True)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()