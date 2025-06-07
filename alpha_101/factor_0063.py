import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delta, ts_sum, add, multiply, subtract, divide, adv

def factor_0063(data, **kwargs):
    """
    数学表达式: ((rank(ts_corr(ts_sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054), ts_sum(adv120, 12.7054), 16.6208)) < rank(ts_delta(((((high + low) / 2) * 0.178404) + (vwap * (1 - 0.178404))), 3.69741))) * -1)
    中文描述: 该因子计算股票过去一段时间的开盘价和最低价的加权平均与成交量加权平均价的加权平均之间的变化，并与过去一段时间的开盘价和最低价的加权平均与未来一段时间的成交额的相关性进行比较，数值小的股票排名靠前，做空；数值大的股票排名靠后，做多。应用场景：1. 识别短期内量价关系异常的股票，例如，价格变化与成交额变化不一致的股票。2. 用于构建量价组合策略，捕捉市场短期内的非理性行为。3. 可作为其他复杂因子或机器学习模型的输入特征，提高模型预测能力。
    """
    # 1. 计算 (open * 0.178404)
    open_weighted = multiply(data['open'], 0.178404)
    # 2. 计算 (low * (1 - 0.178404))
    low_weighted = multiply(data['low'], (1 - 0.178404))
    # 3. 计算 ((open * 0.178404) + (low * (1 - 0.178404)))
    sum_open_low = add(open_weighted, low_weighted)
    # 4. 计算 ts_sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054)
    ts_sum_open_low = ts_sum(sum_open_low, d=12.7054)

    # 为了计算adv120，需要先计算adv
    adv120 = adv(data['vol'],120)
    data['adv120'] = adv120
    # 5. 计算 ts_sum(adv120, 12.7054)
    ts_sum_adv120 = ts_sum(data['adv120'], d=12.7054)
    # 6. 计算 ts_corr(ts_sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054), ts_sum(adv120, 12.7054), 16.6208)
    ts_corr_factor = ts_corr(ts_sum_open_low, ts_sum_adv120, d=16.6208)
    # 7. 计算 rank(ts_corr(ts_sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054), ts_sum(adv120, 12.7054), 16.6208))
    rank_corr = rank(ts_corr_factor, rate = 2)

    # 8. 计算 ((high + low) / 2)
    high_low_mean = divide(add(data['high'], data['low']), 2)
    # 9. 计算 (((high + low) / 2) * 0.178404)
    high_low_mean_weighted = multiply(high_low_mean, 0.178404)
    # 10. 计算 (vwap * (1 - 0.178404))
    vwap_weighted = multiply(data['vwap'], (1 - 0.178404))
    # 11. 计算 ((((high + low) / 2) * 0.178404) + (vwap * (1 - 0.178404)))
    sum_high_low_vwap = add(high_low_mean_weighted, vwap_weighted)
    # 12. 计算 ts_delta(((((high + low) / 2) * 0.178404) + (vwap * (1 - 0.178404))), 3.69741)
    ts_delta_factor = ts_delta(sum_high_low_vwap, d=3.69741)
    # 13. 计算 rank(ts_delta(((((high + low) / 2) * 0.178404) + (vwap * (1 - 0.178404))), 3.69741))
    rank_delta = rank(ts_delta_factor, rate = 2)

    # 14. 计算 (rank(ts_corr(...)) < rank(ts_delta(...)))
    compare_rank = rank_corr < rank_delta
    # 15. 计算 ((rank(ts_corr(...)) < rank(ts_delta(...))) * -1)
    factor = multiply(compare_rank, -1)
    
    del data['adv120']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()