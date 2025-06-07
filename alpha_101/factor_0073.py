import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_sum, multiply, add, subtract, adv

def factor_0073(data, **kwargs):
    """
    数学表达式: ((rank(ts_corr(close, ts_sum(adv30, 37.4843), 15.1365)) < rank(ts_corr(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791))) * -1)
    中文描述: 该因子计算的是一个排序比较的结果，首先计算过去15.1365天收盘价与过去37.4843天平均成交额之和的时间序列相关系数，然后对这个相关系数进行排序；同时，计算一个复杂的表达式与成交量的相关性，该表达式是0.0261661倍的最高价加上(1-0.0261661)倍的平均成交价，再对这个结果和成交量分别进行排序，计算过去11.4791天排序后的相关系数。最后，比较这两个相关系数排序的大小，如果第一个相关系数的排序小于第二个相关系数的排序，则结果为-1，否则为0。该因子可能用于捕捉价格与成交量之间的复杂关系，可以用于构建量价相关的交易策略，例如，可以结合动量策略，在因子值较低时买入，或者用于识别市场异常行为，例如，因子值持续较高可能表明市场存在过度投机。也可以用于高频交易中，快速判断股票的短期趋势。
    因子应用场景：
    1. 量价关系分析：用于识别价格与成交量之间的复杂关系，辅助判断市场趋势。
    2. 交易策略构建：可结合动量策略，在因子值较低时买入。
    3. 市场异常行为识别：因子值持续较高可能表明市场存在过度投机。
    """
    # 计算 adv30 (假设adv30是过去30天平均成交量，这里使用ts_sum(vol, 30)/30来近似)
    adv30 = adv(data['vol'],30)
    data['adv30'] = adv30

    # 1. 计算 ts_sum(adv30, 37.4843)
    data_ts_sum = ts_sum(data['adv30'], d=37)

    # 2. 计算 ts_corr(close, ts_sum(adv30, 37.4843), 15.1365)
    data_ts_corr1 = ts_corr(data['close'], data_ts_sum, d=15)

    # 3. 计算 rank(ts_corr(close, ts_sum(adv30, 37.4843), 15.1365))
    rank1 = rank(data_ts_corr1, rate = 2)

    # 4. 计算 (high * 0.0261661)
    high_multiplied = multiply(data['high'], 0.0261661)

    # 5. 计算 (vwap * (1 - 0.0261661))
    vwap_multiplied = multiply(data['vwap'], (1 - 0.0261661))

    # 6. 计算 ((high * 0.0261661) + (vwap * (1 - 0.0261661)))
    sum_expression = add(high_multiplied, vwap_multiplied)

    # 7. 计算 rank(((high * 0.0261661) + (vwap * (1 - 0.0261661))))
    rank_expression = rank(sum_expression, rate = 2)

    # 8. 计算 rank(volume)
    rank_volume = rank(data['vol'], rate = 2)

    # 9. 计算 ts_corr(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791)
    data_ts_corr2 = ts_corr(rank_expression, rank_volume, d=11)

    # 10. 计算 rank(ts_corr(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791))
    rank2 = rank(data_ts_corr2, rate = 2)

    # 11. 计算 (rank(ts_corr(close, ts_sum(adv30, 37.4843), 15.1365)) < rank(ts_corr(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791)))
    comparison = (rank1 < rank2).astype(int)

    # 12. 计算 ((rank(ts_corr(close, ts_sum(adv30, 37.4843), 15.1365)) < rank(ts_corr(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791))) * -1)
    factor = multiply(comparison, -1)

    # 删除中间变量
    del data['adv30']
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()