import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_decay_linear, ts_std_dev, ts_delta

def factor_6109(data, **kwargs):
    """
    因子名称: VolatilityDecayCorrelation_92302
    数学表达式: ts_corr(ts_decay_linear(ts_std_dev(close, 5), 10), ts_decay_linear(ts_delta(open, 1), 10), 10)
    中文描述: 该因子计算过去10天内收盘价短期波动率线性衰减值与开盘价日变化线性衰减值之间的相关性。首先，利用`ts_std_dev(close, 5)`计算过去5天的收盘价标准差，衡量短期波动性。然后，使用`ts_decay_linear`对短期波动率和开盘价的日变化`ts_delta(open, 1)`进行线性衰减处理，赋予近期数据更高的权重。最后，计算这两个衰减序列在过去10天内的相关性。该因子创新性地结合了短期波动率和价格变化，并引入线性衰减来突出近期市场行为的影响，通过相关性捕捉波动性和价格动量之间的动态关系。相较于参考因子仅关注单一变量的排名或最小值位置，以及历史输出因子简单地对排名进行相关性分析，该因子通过计算波动率和价格变化，并使用线性衰减和相关性操作符，提供了更复杂的市场分析视角，旨在提高因子的预测能力和稳定性，借鉴了改进建议中关于引入波动率指标、使用衰减操作符和相关性操作符的思路。
    因子应用场景：
    1. 趋势识别：因子值较高可能意味着短期波动率和开盘价变化之间存在较强的正相关性，表明市场趋势可能较为明确。
    2. 市场情绪分析：通过分析波动率和价格变化的相关性，可以辅助判断市场情绪，例如，当波动率上升且与价格变化呈正相关时，可能反映市场风险偏好较高。
    """
    # 1. 计算 ts_std_dev(close, 5)
    data_ts_std_dev = ts_std_dev(data['close'], 5)
    # 2. 计算 ts_decay_linear(ts_std_dev(close, 5), 10)
    data_ts_decay_linear_std = ts_decay_linear(data_ts_std_dev, 10)
    # 3. 计算 ts_delta(open, 1)
    data_ts_delta_open = ts_delta(data['open'], 1)
    # 4. 计算 ts_decay_linear(ts_delta(open, 1), 10)
    data_ts_decay_linear_delta = ts_decay_linear(data_ts_delta_open, 10)
    # 5. 计算 ts_corr(ts_decay_linear(ts_std_dev(close, 5), 10), ts_decay_linear(ts_delta(open, 1), 10), 10)
    factor = ts_corr(data_ts_decay_linear_std, data_ts_decay_linear_delta, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()