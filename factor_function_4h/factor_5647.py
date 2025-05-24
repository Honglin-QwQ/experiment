import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, divide, ts_sum, ts_skewness, multiply

def factor_5647(data, **kwargs):
    """
    因子名称: factor_0002_28804
    数学表达式: ts_delta(divide(ts_sum(tbase, 10), ts_sum(tquote, 10)), 2) * ts_skewness(ts_delta(divide(tbase, tquote), 1), 5)
    中文描述: 该因子结合了短期买卖力量变化和中期买卖力量变化偏度。首先，计算过去10天主动买入的基础币种数量总和与主动买入的计价币种数量总和的比率，然后计算该比率在过去2天内的变化，以此捕捉短期买卖力量的变化趋势。其次，计算每日主动买入的基础币种数量与主动买入的计价币种数量的比率的1日差分，并计算该差分在过去5天内的偏度，以此衡量中期买卖力量变化分布的偏斜程度。将两者相乘，旨在识别短期买卖力量变化趋势与中期买卖力量变化分布偏斜程度一致的情况，可能指示更强的趋势持续性。这种创新在于结合了短期趋势和中期分布形态，以更全面地评估市场买卖力量。
    因子应用场景：
    1. 买卖力量趋势识别：用于识别短期买卖力量的变化趋势。
    2. 市场偏斜程度评估：用于衡量中期买卖力量变化分布的偏斜程度。
    3. 趋势持续性判断：结合短期趋势和中期分布形态，评估市场买卖力量的持续性。
    """
    # 1. 计算 ts_sum(tbase, 10)
    data_ts_sum_tbase = ts_sum(data['tbase'], 10)
    # 2. 计算 ts_sum(tquote, 10)
    data_ts_sum_tquote = ts_sum(data['tquote'], 10)
    # 3. 计算 divide(ts_sum(tbase, 10), ts_sum(tquote, 10))
    data_divide_sum = divide(data_ts_sum_tbase, data_ts_sum_tquote)
    # 4. 计算 ts_delta(divide(ts_sum(tbase, 10), ts_sum(tquote, 10)), 2)
    data_ts_delta_divide = ts_delta(data_divide_sum, 2)
    # 5. 计算 divide(tbase, tquote)
    data_divide_tbase_tquote = divide(data['tbase'], data['tquote'])
    # 6. 计算 ts_delta(divide(tbase, tquote), 1)
    data_ts_delta_tbase_tquote = ts_delta(data_divide_tbase_tquote, 1)
    # 7. 计算 ts_skewness(ts_delta(divide(tbase, tquote), 1), 5)
    data_ts_skewness = ts_skewness(data_ts_delta_tbase_tquote, 5)
    # 8. 计算 ts_delta(divide(ts_sum(tbase, 10), ts_sum(tquote, 10)), 2) * ts_skewness(ts_delta(divide(tbase, tquote), 1), 5)
    factor = multiply(data_ts_delta_divide, data_ts_skewness)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()