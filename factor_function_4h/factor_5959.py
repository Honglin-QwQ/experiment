import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, divide, ts_delta, ts_min_diff, ts_std_dev

def factor_5959(data, **kwargs):
    """
    因子名称: VolatilityAdjusted_CloseMinDiff_Ratio_Ranked_90322
    数学表达式: ts_rank(divide(ts_delta(close, 1), divide(ts_min_diff(close, 77), ts_std_dev(close, 20))), 10)
    中文描述: 该因子在参考因子 VolatilityAdjusted_CloseMinDiff_Ratio 的基础上进行了创新，通过引入 ts_rank 运算符，将原始因子的值转换为其在过去10个交易日内的排名。原始因子衡量了短期价格动量相对于经过波动率调整的长期底部差异的强度。通过排名，该因子不再关注原始因子的绝对值，而是其相对强度，这有助于消除量纲差异并提高因子的可比性。当原始因子在过去10天内排名靠前时，表明当前的价格动量相对于波动率调整后的长期底部差异非常强劲，可能预示着持续的上涨潜力。该因子结合了参考因子中的close和ts_min_diff，并引入了ts_delta、divide、ts_std_dev和ts_rank运算符，通过对波动率调整后的比率进行排名来捕捉相对强度，以期提升因子的稳定性和预测能力。这响应了改进建议中关于引入波动率影响和使用收益率而非价格差（尽管这里是波动率调整，逻辑相似）以及优化参数（ts_std_dev的时间窗口）的建议，并利用了divide、ts_std_dev和ts_rank操作符来提升因子。相较于原始因子，排名处理是主要的创新点，旨在应对原始因子IC波动性大的问题，通过关注相对位置而非绝对值来平滑因子表现。
    因子应用场景：
    1. 动量分析：用于识别短期价格动量相对于波动率调整后的长期底部差异的相对强度。
    2. 趋势跟踪：当因子排名较高时，可能预示着价格上涨趋势的持续。
    3. 风险调整：通过波动率调整，该因子有助于在不同波动率环境下的股票之间进行比较。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta = ts_delta(data['close'], 1)
    # 2. 计算 ts_min_diff(close, 77)
    data_ts_min_diff = ts_min_diff(data['close'], 77)
    # 3. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 4. 计算 divide(ts_min_diff(close, 77), ts_std_dev(close, 20))
    data_divide_min_std = divide(data_ts_min_diff, data_ts_std_dev)
    # 5. 计算 divide(ts_delta(close, 1), divide(ts_min_diff(close, 77), ts_std_dev(close, 20)))
    data_divide = divide(data_ts_delta, data_divide_min_std)
    # 6. 计算 ts_rank(divide(ts_delta(close, 1), divide(ts_min_diff(close, 77), ts_std_dev(close, 20))), 10)
    factor = ts_rank(data_divide, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()