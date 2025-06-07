import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_max, ts_corr, ts_rank, indneutralize, adv, multiply, subtract

def factor_0089(data, **kwargs):
    """
    数学表达式: ((rank((close - ts_max(close, 4.66719)))^ts_rank(ts_corr(indneutralize(adv40, IndClass.subindustry), low, 5.38375), 3.21856)) * -1) 
    中文描述: 详细描述：该因子首先计算过去4.66719天收盘价的最大值，然后用当前收盘价减去该最大值，并对结果进行排序。接着，计算过去5.38375天成交额40日均值与最低价的相关性，对该相关性进行过去3.21856天的排名。最后，将收盘价差值的排序与相关性排名的乘积取负值，再进行排序。该因子试图捕捉价格在短期内相对于近期高点的变化趋势，并结合成交额与价格波动关系，寻找被低估或高估的股票。因子值越大，可能表示股票价格相对于其近期高点较低，且成交额与价格的相关性较高，可能存在反弹机会。 因子应用场景：1. 趋势反转策略：当因子值较高时，买入股票，预期价格将从低点反弹。2. 动量衰减策略：当因子值持续下降时，卖出股票，预期价格将继续下跌。3. 结合其他因子：与其他基本面或技术面因子结合，例如盈利能力、市盈率等，构建更稳健的选股模型。
    """
    # 1. 计算 ts_max(close, 4.66719)
    data_ts_max_close = ts_max(data['close'], d = 4.66719)
    # 2. 计算 (close - ts_max(close, 4.66719))
    data_close_diff = subtract(data['close'], data_ts_max_close)
    # 3. 计算 rank((close - ts_max(close, 4.66719)))
    data_rank_close_diff = rank(data_close_diff, rate = 2)
    # 4. 计算 adv40(data['amount'])
    data_adv40 = adv(data['amount'],40)
    # 5. 计算 indneutralize(adv40, IndClass.subindustry)
    data_ind_neutralize = indneutralize(data_adv40, data['industry'])
    # 6. 计算 ts_corr(indneutralize(adv40, IndClass.subindustry), low, 5.38375)
    data_ts_corr = ts_corr(data_ind_neutralize, data['low'], d = 5.38375)
    # 7. 计算 ts_rank(ts_corr(indneutralize(adv40, IndClass.subindustry), low, 5.38375), 3.21856)
    data_ts_rank = ts_rank(data_ts_corr, d = 3.21856)
    # 8. 计算 (rank((close - ts_max(close, 4.66719)))^ts_rank(ts_corr(indneutralize(adv40, IndClass.subindustry), low, 5.38375), 3.21856))
    data_signed_power = data_rank_close_diff ** data_ts_rank
    # 9. 计算 ((rank((close - ts_max(close, 4.66719)))^ts_rank(ts_corr(indneutralize(adv40, IndClass.subindustry), low, 5.38375), 3.21856)) * -1)
    factor = multiply(data_signed_power, -1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()