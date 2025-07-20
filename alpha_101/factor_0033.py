import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_std_dev, ts_delta, subtract, add

def factor_0033(data, **kwargs):
    """
    数学表达式: rank(((1 - rank((ts_std_dev(returns, 2) / ts_std_dev(returns, 5)))) + (1 - rank(ts_delta(close, 1)))))
    中文描述: 描述：该因子首先计算过去2天收益率标准差与过去5天收益率标准差的比率，然后对该比率进行排序，并用1减去排序结果。接着，计算收盘价1日的变化量，并对其进行排序，再用1减去排序结果。最后，将前述两个结果相加，并对总和进行排序，得到最终的因子值。该因子衡量了近期收益率波动率的相对变化以及价格动量的反向排序组合，数值越小可能代表股票近期波动率相对较低且价格下跌动能较弱，反之亦然。
    应用场景：
    1. 可以用于构建低波动率选股策略，选取因子值较低的股票，预期这些股票未来波动较小。
    2. 可以与动量策略结合，当因子值较低时，表明股票可能处于超卖状态，结合其他技术指标，寻找买入机会。
    3. 可以作为机器学习模型的输入特征，用于预测股票收益率或风险水平，帮助模型更好地理解市场动态。
    """
    # 1. 计算 ts_std_dev(returns, 2)
    data_ts_std_dev_2 = ts_std_dev(data['returns'], 2)
    # 2. 计算 ts_std_dev(returns, 5)
    data_ts_std_dev_5 = ts_std_dev(data['returns'], 5)
    # 3. 计算 (ts_std_dev(returns, 2) / ts_std_dev(returns, 5))
    data_divide = data_ts_std_dev_2 / data_ts_std_dev_5
    # 4. 计算 rank((ts_std_dev(returns, 2) / ts_std_dev(returns, 5)))
    data_rank_1 = rank(data_divide, 2)
    # 5. 计算 (1 - rank((ts_std_dev(returns, 2) / ts_std_dev(returns, 5))))
    data_subtract_1 = subtract(1, data_rank_1)
    # 6. 计算 ts_delta(close, 1)
    data_ts_delta_1 = ts_delta(data['close'], 1)
    # 7. 计算 rank(ts_delta(close, 1))
    data_rank_2 = rank(data_ts_delta_1, 2)
    # 8. 计算 (1 - rank(ts_delta(close, 1)))
    data_subtract_2 = subtract(1, data_rank_2)
    # 9. 计算 ((1 - rank((ts_std_dev(returns, 2) / ts_std_dev(returns, 5)))) + (1 - rank(ts_delta(close, 1))))
    data_add = add(data_subtract_1, data_subtract_2)
    # 10. 计算 rank(((1 - rank((ts_std_dev(returns, 2) / ts_std_dev(returns, 5)))) + (1 - rank(ts_delta(close, 1)))))
    factor = rank(data_add, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()