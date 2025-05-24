import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, fraction, kth_element, divide

def factor_5699(data, **kwargs):
    """
    因子名称: LogDiff_High_Fraction_KthElement_Ratio_53862
    数学表达式: divide(log_diff(high), fraction(kth_element(high, 5, k=1)))
    中文描述: 该因子结合了对数差分和分形的概念，旨在捕捉最高价的相对变化与短期历史最高价小数部分的比例关系。首先计算当前最高价的对数差分，反映了最高价的相对变化率。然后计算过去5天内最高价的第1个元素（即5天前的最高价）的小数部分。最后，将对数差分除以该小数部分。这个因子创新性地将价格变化率与历史价格的细微结构相结合，可能用于识别在特定历史价格水平附近出现的价格变化加速或减缓的信号。如果比例较高，可能表示当前最高价的相对变化较大，且发生在历史最高价的小数部分较小的位置，这可能暗示着价格突破或趋势的强化。反之，如果比例较低，可能表示当前最高价的相对变化较小，或者发生在历史最高价小数部分较大的位置，可能暗示着价格在历史高位附近遇到阻力或盘整。该因子适用于捕捉短期内价格在历史高点附近的精细波动特征。
    因子应用场景：
    1. 识别价格变化加速或减缓的信号。
    2. 判断价格突破或趋势强化的可能性。
    3. 评估价格在历史高位附近遇到的阻力或盘整。
    """
    # 1. 计算 log_diff(high)
    data_log_diff_high = log_diff(data['high'])
    # 2. 计算 kth_element(high, 5, k=1)
    data_kth_element_high = kth_element(data['high'], d=5, k=1)
    # 3. 计算 fraction(kth_element(high, 5, k=1))
    data_fraction_kth_element_high = fraction(data_kth_element_high)
    # 4. 计算 divide(log_diff(high), fraction(kth_element(high, 5, k=1)))
    factor = divide(data_log_diff_high, data_fraction_kth_element_high)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()