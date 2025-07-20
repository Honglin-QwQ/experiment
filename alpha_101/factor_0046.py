import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, divide, multiply, subtract, ts_sum, ts_delay, adv

def factor_0046(data, **kwargs):
    """
    数学表达式: ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (ts_sum(high, 5) / 5))) - rank((vwap - ts_delay(vwap, 5))))
    中文描述: 描述：首先计算收盘价倒数的排序，再乘以成交量，并除以过去20日平均成交额；然后计算最高价与最高价减收盘价差值的排序的乘积，再除以过去5日最高价的平均值；将两部分相乘，最后减去成交量加权平均价与5日前成交量加权平均价差值的排序。该因子结合了价格、成交量和时间序列信息，旨在捕捉短期价格动量和成交量变化的关系。
    应用场景：
    1. 短线择时：因子值较高可能预示着股价上涨的动能较强，可作为买入信号；因子值较低可能预示着股价下跌的动能较强，可作为卖出信号。
    2. 量化选股：将该因子与其他基本面因子、技术因子结合，构建多因子选股模型，筛选出具有较高潜在收益的股票。
    3. 异动捕捉：监控因子值的异常变化，例如因子值突然大幅上升，可能表明市场对该股票的关注度增加，存在交易机会。
    """
    # 1. 计算 (1 / close)
    inv_close = divide(1, data['close'])
    # 2. 计算 rank((1 / close))
    rank_inv_close = rank(inv_close)
    # 3. 计算 rank((1 / close)) * volume
    rank_inv_close_volume = multiply(rank_inv_close, data['vol'])
    # 4. 计算 adv20
    adv20 = adv(data['vol'], d = 20)
    # 5. 计算 ((rank((1 / close)) * volume) / adv20)
    term1 = divide(rank_inv_close_volume, adv20)
    # 6. 计算 (high - close)
    high_minus_close = subtract(data['high'], data['close'])
    # 7. 计算 rank((high - close))
    rank_high_minus_close = rank(high_minus_close)
    # 8. 计算 (high * rank((high - close)))
    high_rank_high_minus_close = multiply(data['high'], rank_high_minus_close)
    # 9. 计算 ts_sum(high, 5)
    ts_sum_high_5 = ts_sum(data['high'], d = 5)
    # 10. 计算 (ts_sum(high, 5) / 5)
    ts_sum_high_5_div_5 = divide(ts_sum_high_5, 5)
    # 11. 计算 ((high * rank((high - close))) / (ts_sum(high, 5) / 5))
    term2 = divide(high_rank_high_minus_close, ts_sum_high_5_div_5)
    # 12. 计算 ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (ts_sum(high, 5) / 5)))
    term1_mult_term2 = multiply(term1, term2)
    # 13. 计算 ts_delay(vwap, 5)
    ts_delay_vwap_5 = ts_delay(data['vwap'], d = 5)
    # 14. 计算 (vwap - ts_delay(vwap, 5))
    vwap_minus_ts_delay_vwap_5 = subtract(data['vwap'], ts_delay_vwap_5)
    # 15. 计算 rank((vwap - ts_delay(vwap, 5)))
    rank_vwap_minus_ts_delay_vwap_5 = rank(vwap_minus_ts_delay_vwap_5)
    # 16. 计算 ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (ts_sum(high, 5) / 5))) - rank((vwap - ts_delay(vwap, 5))))
    factor = subtract(term1_mult_term2, rank_vwap_minus_ts_delay_vwap_5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()