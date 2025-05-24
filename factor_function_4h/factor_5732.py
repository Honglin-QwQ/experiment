import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_decay_linear, log_diff, ts_decay_exp_window

def factor_5732(data, **kwargs):
    """
    因子名称: WeightedLogDiffHigh_VolRatio_20282
    数学表达式: divide(ts_decay_linear(log_diff(high), d=5), ts_decay_exp_window(vol, d=10, factor=0.5))
    中文描述: 该因子旨在捕捉近期最高价对数差分的线性衰减加权平均与近期成交量指数衰减加权平均的比例关系。首先计算当前最高价的对数差分，反映了最高价的相对变化率。然后计算过去5天最高价对数差分的线性衰减加权平均，给予近期变化更高的权重。同时，计算过去10天成交量的指数衰减加权平均，给予近期成交量更高的权重。最后，将线性衰减加权的最高价对数差分除以指数衰减加权的成交量。这个因子在历史输出的基础上进行了改进，通过引入最高价对数差分的线性衰减加权平均，更精细地捕捉了近期价格变化的趋势，并将其与近期加权成交量相结合。这种结合方式可能用于识别在不同成交活跃度背景下，近期价格变化的强度和方向。如果比例较高，可能表示近期最高价的相对变化较大且呈线性衰减趋势，同时发生在近期成交量加权平均较低的位置，这可能暗示着价格在相对缺乏成交支持的情况下出现较强的动量。反之，如果比例较低，可能表示近期最高价的相对变化较小或者发生在近期成交量加权平均较高的位置，可能暗示着价格在成交活跃的情况下动量较弱或处于盘整。该因子适用于捕捉短期内价格动量与近期成交量模式的相互作用，并在历史输出的基础上尝试提升因子的预测能力和稳定性。
    因子应用场景：
    1. 动量识别：用于识别在成交量较低的情况下，价格动量较强的股票。
    2. 趋势确认：结合成交量变化，验证价格趋势的可靠性。
    3. 市场情绪分析：通过观察因子值与市场整体表现的关系，评估市场情绪。
    """
    # 1. 计算 log_diff(high)
    data_log_diff_high = log_diff(data['high'])
    # 2. 计算 ts_decay_linear(log_diff(high), d=5)
    data_ts_decay_linear = ts_decay_linear(data_log_diff_high, d=5)
    # 3. 计算 ts_decay_exp_window(vol, d=10, factor=0.5)
    data_ts_decay_exp_window = ts_decay_exp_window(data['vol'], d=10, factor=0.5)
    # 4. 计算 divide(ts_decay_linear(log_diff(high), d=5), ts_decay_exp_window(vol, d=10, factor=0.5))
    factor = divide(data_ts_decay_linear, data_ts_decay_exp_window)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()