import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_min, rank, ts_decay_linear, ts_delta, ts_rank, ts_corr, indneutralize, add, multiply, subtract, min

def factor_0081(data, **kwargs):
    """
    数学表达式: (ts_min(rank(ts_decay_linear(ts_delta(open, 1.46063), 14.8717)), ts_rank(ts_decay_linear(ts_corr(indneutralize(volume, IndClass.sector), ((open * 0.634196) + (open * (1 - 0.634196))), 17.4842), 6.92131), 13.4283)) * -1)
    中文描述: 该因子首先计算过去1.46063天开盘价的变化，然后计算该变化值在过去14.8717天内的线性衰减值，并对衰减值进行排序，取过去所有排序中的最小值；另一部分，先对成交量进行行业中性化处理，再计算行业中性化成交量与开盘价加权平均（权重为0.634196和1-0.634196）在过去17.4842天内的相关性，然后计算该相关性在过去6.92131天内的线性衰减值，并对衰减值进行排序，最后取排序的名次，将该名次取反；最终，该因子取两部分的最小值。
    应用场景：
    1. 可以用于识别短期开盘价变化较小且成交量与开盘价相关性较弱的股票。
    2. 可以用于构建量化交易策略，例如，选择因子值较低的股票进行买入。
    3. 可以与其他因子结合使用，提高选股效果。
    """
    # 1. 计算 ts_delta(open, 1.46063)
    data_ts_delta_open = ts_delta(data['open'], 1.46063)
    # 2. 计算 ts_decay_linear(ts_delta(open, 1.46063), 14.8717)
    data_ts_decay_linear = ts_decay_linear(data_ts_delta_open, 14.8717)
    # 3. 计算 rank(ts_decay_linear(ts_delta(open, 1.46063), 14.8717))
    data_rank = rank(data_ts_decay_linear)
    # 4. 计算 indneutralize(volume, IndClass.sector)
    data_indneutralize = indneutralize(data['vol'], data['industry'])
    # 5. 计算 (open * 0.634196) + (open * (1 - 0.634196))
    data_open_weighted_avg = add(multiply(data['open'], 0.634196), multiply(data['open'], (1 - 0.634196)))
    # 6. 计算 ts_corr(indneutralize(volume, IndClass.sector), ((open * 0.634196) + (open * (1 - 0.634196))), 17.4842)
    data_ts_corr = ts_corr(data_indneutralize, data_open_weighted_avg, 17.4842)
    # 7. 计算 ts_decay_linear(ts_corr(indneutralize(volume, IndClass.sector), ((open * 0.634196) + (open * (1 - 0.634196))), 17.4842), 6.92131)
    data_ts_decay_linear_corr = ts_decay_linear(data_ts_corr, 6.92131)
    # 8. 计算 ts_rank(ts_decay_linear(ts_corr(indneutralize(volume, IndClass.sector), ((open * 0.634196) + (open * (1 - 0.634196))), 17.4842), 6.92131), 13.4283)
    data_ts_rank = ts_rank(data_ts_decay_linear_corr, 13.4283)
    # 9. 计算 ts_rank(ts_decay_linear(ts_corr(indneutralize(volume, IndClass.sector), ((open * 0.634196) + (open * (1 - 0.634196))), 17.4842), 6.92131), 13.4283) * -1
    data_ts_rank_neg = multiply(data_ts_rank, -1)
    # 10. 计算 ts_min(rank(ts_decay_linear(ts_delta(open, 1.46063), 14.8717)), ts_rank(ts_decay_linear(ts_corr(indneutralize(volume, IndClass.sector), ((open * 0.634196) + (open * (1 - 0.634196))), 17.4842), 6.92131), 13.4283) * -1)
    factor = min(data_rank, data_ts_rank_neg)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()