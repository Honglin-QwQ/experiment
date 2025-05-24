import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_decay_linear, kth_element, ts_arg_max, ts_delay

def factor_5808(data, **kwargs):
    """
    因子名称: Volume_Peak_Decay_Open_Ratio_15979
    数学表达式: divide(ts_decay_linear(kth_element(vol, 5, k=1) * ts_arg_max(vol, 3), 10), ts_delay(open, 60))
    中文描述: 该因子结合了短期交易量峰值信息和长期开盘价信息。首先，它在过去5天内找到一个有效的交易量数据（可能是最近的），并将其乘以该交易量在过去3天内达到最大值的相对索引。这部分旨在捕捉短期内交易量的活跃度和峰值位置。然后，对这个结果进行10天的线性衰减加权平均，以平滑短期波动并引入一定的记忆效应。最后，将这个衰减后的交易量峰值指标除以60天前的开盘价。这个除法操作将短期交易量行为与长期价格水平进行对比，可能揭示市场情绪的短期爆发是否得到长期价格趋势的支撑。例如，如果短期交易量峰值指标相对较高，而60天前的开盘价较低，可能意味着当前市场情绪高涨，并且相对于长期价格水平有显著的提升，这可能是一个潜在的买入信号。创新点在于结合了kth_element用于数据处理、ts_arg_max捕捉峰值位置、ts_decay_linear进行平滑和记忆，以及与长期开盘价的比例关系，形成一个多维度捕捉短期交易量异常与长期价格对比的因子。
    因子应用场景：
    1. 市场情绪分析：用于识别短期交易量激增相对于长期价格水平的异常情况。
    2. 买卖信号：当因子值较高时，可能表明市场情绪高涨，是潜在的买入信号。
    """
    # 1. 计算 kth_element(vol, 5, k=1)
    data_kth_element = kth_element(data['vol'], 5, k=1)
    # 2. 计算 ts_arg_max(vol, 3)
    data_ts_arg_max = ts_arg_max(data['vol'], 3)
    # 3. 计算 kth_element(vol, 5, k=1) * ts_arg_max(vol, 3)
    data_multiply = data_kth_element * data_ts_arg_max
    # 4. 计算 ts_decay_linear(kth_element(vol, 5, k=1) * ts_arg_max(vol, 3), 10)
    data_ts_decay_linear = ts_decay_linear(data_multiply, 10)
    # 5. 计算 ts_delay(open, 60)
    data_ts_delay = ts_delay(data['open'], 60)
    # 6. 计算 divide(ts_decay_linear(kth_element(vol, 5, k=1) * ts_arg_max(vol, 3), 10), ts_delay(open, 60))
    factor = divide(data_ts_decay_linear, data_ts_delay)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()