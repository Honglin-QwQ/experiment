import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_entropy

def factor_5772(data, **kwargs):
    """
    因子名称: Volume_Price_Entropy_Correlation_61020
    数学表达式: ts_corr(ts_entropy(vol, 10), ts_entropy(close, 10), 5)
    中文描述: 该因子计算过去10天成交量和收盘价各自的信息熵，然后计算这两个信息熵在过去5天内的相关性。信息熵衡量了序列的随机性或无序程度。
            该因子通过分析量价序列的随机性之间的相关性，来捕捉市场潜在的结构性变化。例如，当量价熵呈现强烈的正相关时，可能意味着市场处于混沌状态，量价关系不稳定；
            而负相关可能预示着某种趋势的形成。这相对于直接使用量价本身的相关性更具创新性，因为它关注的是量价变化的模式而非具体数值。可以用于识别市场状态、辅助判断趋势的可靠性或作为异动检测指标。
    因子应用场景：
    1. 市场状态识别： 通过量价熵的相关性判断市场是处于混沌状态还是趋势状态。
    2. 趋势可靠性辅助判断： 负相关可能预示着某种趋势的形成，可辅助判断趋势的可靠性。
    3. 异动检测指标： 量价熵相关性的突变可能预示着市场异动。
    """
    # 1. 计算 ts_entropy(vol, 10)
    data_ts_entropy_vol = ts_entropy(data['vol'], 10)
    # 2. 计算 ts_entropy(close, 10)
    data_ts_entropy_close = ts_entropy(data['close'], 10)
    # 3. 计算 ts_corr(ts_entropy(vol, 10), ts_entropy(close, 10), 5)
    factor = ts_corr(data_ts_entropy_vol, data_ts_entropy_close, 5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()