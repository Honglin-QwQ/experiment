import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_delta, ts_decay_exp_window, ts_rank, multiply

def factor_6049(data, **kwargs):
    """
    因子名称: VolatilityAdjustedSkewedMomentum_15954
    数学表达式: ts_skewness(ts_delta(close, 5), 60) * ts_decay_exp_window(ts_rank(vol, 90), 120, factor=0.7)
    中文描述: 该因子是一个创新的动量因子，结合了短期价格变化的偏度与经过指数衰减加权处理的长期成交量排名。因子表达式首先计算过去5天收盘价变化的偏度在过去60天内的滚动值。偏度衡量了收益率分布的非对称性，正偏度表示存在较大的正向极端收益的可能性，负偏度则表示存在较大的负向极端收益的可能性。这一部分旨在捕捉价格动量中隐藏的风险或机会信息。创新点在于引入了经过指数衰减加权处理的长期成交量排名。首先计算过去90天成交量的排名，然后对这个排名应用120天窗口的指数衰减加权平均，衰减因子设置为0.7。这样做可以使近期成交量排名的影响更大，同时保留部分长期信息，并且通过指数衰减平滑数据，减少噪声。最后，将价格变化偏度与经过处理的长期成交量排名相乘。这个组合因子试图识别那些在特定偏度（潜在的上涨或下跌风险）下，伴随着特定模式（近期权重更大）的长期成交量行为的股票。相较于简单的价格动量或成交量因子，它引入了对收益分布形态的考量和更精细的长期成交量处理方式，可能有助于发现更复杂的市场信号。
    因子应用场景：
    1. 动量反转：当因子值较高时，可能预示着超买状态，未来可能出现价格反转。
    2. 风险评估：结合偏度和成交量信息，可以评估市场潜在的风险水平。
    3. 选股策略：用于识别具有特定偏度和成交量模式的股票，构建更稳健的投资组合。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 2. 计算 ts_skewness(ts_delta(close, 5), 60)
    data_ts_skewness = ts_skewness(data_ts_delta_close, 60)
    # 3. 计算 ts_rank(vol, 90)
    data_ts_rank_vol = ts_rank(data['vol'], 90)
    # 4. 计算 ts_decay_exp_window(ts_rank(vol, 90), 120, factor=0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_rank_vol, 120, factor=0.7)
    # 5. 计算 ts_skewness(ts_delta(close, 5), 60) * ts_decay_exp_window(ts_rank(vol, 90), 120, factor=0.7)
    factor = multiply(data_ts_skewness, data_ts_decay_exp_window)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()