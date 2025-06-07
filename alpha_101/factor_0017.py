import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_std_dev, subtract, add, abs, multiply

def factor_0017(data, **kwargs):
    """
    数学表达式: (-1 * rank(((ts_std_dev(abs((close - open)), 5) + (close - open)) + ts_corr(close, open, 10))))
    中文描述: 该因子首先计算过去5天收盘价减去开盘价绝对值的标准差，然后加上当日收盘价减去开盘价的差值，再计算收盘价和开盘价过去10天的相关系数，将前两部分相加后与相关系数相加，最后对结果进行排序并取负。这个因子捕捉了价格波动性和价格趋势的相关性，值越小可能代表股票未来收益越高。
    应用场景：
    1. 可以用于构建多因子模型，与其他因子结合使用，提高选股效果。
    2. 可以用于量化对冲策略，选择因子值较低的股票做多，同时做空因子值较高的股票，构建多空组合。
    3. 可以作为动量反转策略的参考，因子值较低的股票可能存在反弹机会。
    """

    # 1. 计算 (close - open)
    close_minus_open = subtract(data['close'], data['open'])

    # 2. 计算 abs((close - open))
    abs_close_minus_open = abs(close_minus_open)

    # 3. 计算 ts_std_dev(abs((close - open)), 5)
    ts_std_dev_abs_close_minus_open = ts_std_dev(abs_close_minus_open, 5)

    # 4. 计算 (ts_std_dev(abs((close - open)), 5) + (close - open))
    std_dev_plus_diff = add(ts_std_dev_abs_close_minus_open, close_minus_open)

    # 5. 计算 ts_corr(close, open, 10)
    ts_corr_close_open = ts_corr(data['close'], data['open'], 10)

    # 6. 计算 ((ts_std_dev(abs((close - open)), 5) + (close - open)) + ts_corr(close, open, 10))
    sum_expression = add(std_dev_plus_diff, ts_corr_close_open)

    # 7. 计算 rank(((ts_std_dev(abs((close - open)), 5) + (close - open)) + ts_corr(close, open, 10))))
    ranked_expression = rank(sum_expression, 2)

    # 8. 计算 -1 * rank(((ts_std_dev(abs((close - open)), 5) + (close - open)) + ts_corr(close, open, 10))))
    factor = multiply(-1, ranked_expression)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()