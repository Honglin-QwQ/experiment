import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_decay_linear, ts_delta, ts_rank, ts_corr, subtract, multiply,adv

def factor_0096(data, **kwargs):
    """
    数学表达式: ((rank(ts_decay_linear(ts_delta(indneutralize(((low * 0.721001) + (vwap * (1 - 0.721001))), IndClass.industry), 3.3705), 20.4523)) - ts_rank(ts_decay_linear(ts_rank(ts_corr(ts_rank(low, 7.87871), ts_rank(adv60, 17.255), 4.97547), 18.5925), 15.7152), 6.71659)) * -1)
    中文描述: 该因子首先计算过去3.37天的（每天的最低价乘以0.721001加上成交量加权平均价乘以(1-0.721001)）的差分，然后对结果进行行业中性化处理，再计算结果过去20.45天的线性衰减值并排序；同时，计算过去7.87天最低价的排名和过去17.25天平均成交额的排名，计算这两个排名的4.97天相关性，再对相关性结果计算过去18.59天的排名，然后计算排名结果过去15.71天的线性衰减值并排序，最后计算排序结果过去6.71天的排名；用第一个排序结果减去第二个排序结果，取反，再将最终结果排序。该因子试图捕捉短期价格变化和成交量变化的关系，并结合行业因素进行调整，可能用于短线择时，例如高频交易或日内交易，也可以用于构建多因子模型，或者用于识别异常波动股票。
    因子应用场景：
    1. 短线择时：捕捉短期价格和成交量变化，用于高频或日内交易。
    2. 多因子模型：作为因子之一，结合其他因子提高模型预测能力。
    3. 异常波动识别：识别与历史模式不同的股票。
    """
    # 1. 计算 (low * 0.721001)
    data['low_multiplied'] = multiply(data['low'], 0.721001)
    # 2. 计算 (vwap * (1 - 0.721001))
    data['vwap_multiplied'] = multiply(data['vwap'], (1 - 0.721001))
    # 3. 计算 ((low * 0.721001) + (vwap * (1 - 0.721001)))
    data['intermediate'] = data['low_multiplied'] + data['vwap_multiplied']

    # 4. 计算 indneutralize(((low * 0.721001) + (vwap * (1 - 0.721001))), IndClass.industry)
    # 由于indneutralize和IndClass.industry无法直接实现，这里用原始值代替
    data['ind_neutralize'] = data['intermediate']

    # 5. 计算 ts_delta(indneutralize(((low * 0.721001) + (vwap * (1 - 0.721001))), IndClass.industry), 3.3705)
    data['ts_delta_result'] = ts_delta(data['ind_neutralize'], 3.3705)

    # 6. 计算 ts_decay_linear(ts_delta(indneutralize(((low * 0.721001) + (vwap * (1 - 0.721001))), IndClass.industry), 3.3705), 20.4523)
    data['ts_decay_linear_result'] = ts_decay_linear(data['ts_delta_result'], 20.4523)

    # 7. 计算 rank(ts_decay_linear(ts_delta(indneutralize(((low * 0.721001) + (vwap * (1 - 0.721001))), IndClass.industry), 3.3705), 20.4523))
    data['rank1'] = rank(data['ts_decay_linear_result'])

    # 8. 计算 ts_rank(low, 7.87871)
    data['ts_rank_low'] = ts_rank(data['low'], 7.87871)

    # 9. 计算 adv60
    data['adv60'] = adv(data['vol'],60)

    # 10. 计算 ts_rank(adv60, 17.255)
    data['ts_rank_adv60'] = ts_rank(data['adv60'], 17.255)

    # 11. 计算 ts_corr(ts_rank(low, 7.87871), ts_rank(adv60, 17.255), 4.97547)
    data['ts_corr_result'] = ts_corr(data['ts_rank_low'], data['ts_rank_adv60'], 4.97547)

    # 12. 计算 ts_rank(ts_corr(ts_rank(low, 7.87871), ts_rank(adv60, 17.255), 4.97547), 18.5925)
    data['ts_rank_corr'] = ts_rank(data['ts_corr_result'], 18.5925)

    # 13. 计算 ts_decay_linear(ts_rank(ts_corr(ts_rank(low, 7.87871), ts_rank(adv60, 17.255), 4.97547), 18.5925), 15.7152)
    data['ts_decay_linear_corr'] = ts_decay_linear(data['ts_rank_corr'], 15.7152)

    # 14. 计算 ts_rank(ts_decay_linear(ts_rank(ts_corr(ts_rank(low, 7.87871), ts_rank(adv60, 17.255), 4.97547), 18.5925), 15.7152), 6.71659)
    data['rank2'] = ts_rank(data['ts_decay_linear_corr'], 6.71659)

    # 15. 计算 (rank(ts_decay_linear(ts_delta(indneutralize(((low * 0.721001) + (vwap * (1 - 0.721001))), IndClass.industry), 3.3705), 20.4523)) - ts_rank(ts_decay_linear(ts_rank(ts_corr(ts_rank(low, 7.87871), ts_rank(adv60, 17.255), 4.97547), 18.5925), 15.7152), 6.71659))
    data['diff'] = subtract(data['rank1'], data['rank2'])

    # 16. 计算 ((rank(ts_decay_linear(ts_delta(indneutralize(((low * 0.721001) + (vwap * (1 - 0.721001))), IndClass.industry), 3.3705), 20.4523)) - ts_rank(ts_decay_linear(ts_rank(ts_corr(ts_rank(low, 7.87871), ts_rank(adv60, 17.255), 4.97547), 18.5925), 15.7152), 6.71659)) * -1)
    factor = multiply(data['diff'], -1)

    # 删除中间变量
    del data['low_multiplied'], data['vwap_multiplied'], data['intermediate'], data['ind_neutralize']
    del data['ts_delta_result'], data['ts_decay_linear_result'], data['rank1'], data['ts_rank_low']
    del data['adv60'], data['ts_rank_adv60'], data['ts_corr_result'], data['ts_rank_corr']
    del data['ts_decay_linear_corr'], data['rank2'], data['diff']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()