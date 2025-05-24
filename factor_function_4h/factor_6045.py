import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, divide, ts_std_dev, ts_decay_linear, ts_rank
import pandas as pd

def factor_6045(data, **kwargs):
    """
    数学表达式: scale(divide(ts_std_dev(vol, 10), ts_decay_linear(ts_rank(vol, 10), 10)))
    中文描述: 该因子是Volume_Volatility_Decay_Ratio_Improved因子的增强版本。它计算过去10天成交量标准差与过去10天成交量排名线性衰减平均值的比值，并对结果进行标准化。相较于前一版本，该因子主要调整了标准差和线性衰减的计算窗口期至10天，以期更好地捕捉中短期市场波动和趋势。此外，它继续沿用了对成交量进行排名后再计算线性衰减平均的方法，以减少异常值影响。该因子旨在识别成交量波动相对较高但近期成交量排名呈现下降趋势的股票，可能用于捕捉市场情绪变化和资金流向的潜在信号，并期望通过调整窗口期提升因子的预测能力和稳定性。
    因子应用场景：
    1. 市场情绪分析：用于识别成交量波动较大但排名下降的股票，可能预示市场情绪转变。
    2. 资金流向跟踪：辅助判断资金流出或流入的迹象，特别是在成交量变化与排名趋势不一致时。
    3. 短期趋势预测：通过调整窗口期，捕捉中短期市场波动和趋势，提高预测能力。
    """
    # 1. 计算 ts_std_dev(vol, 10)
    data_ts_std_dev = ts_std_dev(data['vol'], d = 10)
    # 2. 计算 ts_rank(vol, 10)
    data_ts_rank = ts_rank(data['vol'], d = 10)
    # 3. 计算 ts_decay_linear(ts_rank(vol, 10), 10)
    data_ts_decay_linear = ts_decay_linear(data_ts_rank, d = 10)
    # 4. 计算 divide(ts_std_dev(vol, 10), ts_decay_linear(ts_rank(vol, 10), 10))
    data_divide = divide(data_ts_std_dev, data_ts_decay_linear)
    # 5. 计算 scale(divide(ts_std_dev(vol, 10), ts_decay_linear(ts_rank(vol, 10), 10)))
    factor = scale(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()