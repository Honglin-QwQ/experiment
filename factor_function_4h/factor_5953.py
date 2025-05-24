import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import jump_decay, ts_std_dev, ts_mean, divide

def factor_5953(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Jump_Decay_Ratio_60468
    数学表达式: divide(jump_decay(ts_std_dev(vwap, 10), d=5, sensitivity=0.1, force=0.05), ts_mean(vol, 10))
    中文描述: 该因子旨在捕捉VWAP短期波动率的跳跃衰减特征，并将其与成交量均值进行对比。首先，计算过去10天内VWAP的滚动标准差，反映VWAP的短期波动性。
            然后，应用jump_decay操作符，计算波动率序列在过去5天内相对于历史值的跳跃衰减贡献值，以平滑异常波动。
            最后，将平滑后的波动率跳跃衰减值除以过去10天内的平均成交量。
            当VWAP波动率出现经过平滑处理的显著跳跃且平均成交量较低时，因子值较大，可能预示着在低流动性环境下，价格波动出现异常变化，这可能是一个潜在的市场信号。
            该因子的创新点在于结合了jump_decay操作符来处理波动率序列，并将其与成交量均值进行比率计算，以期发现更复杂的市场模式，并尝试解决历史因子中逻辑复杂且预测能力弱的问题。
    因子应用场景：
    1. 异常波动检测：用于识别VWAP波动率出现显著跳跃且成交量较低的情况，可能预示着市场异常波动。
    2. 低流动性风险预警：当因子值较高时，可能表明市场流动性不足，价格波动风险较高。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev = ts_std_dev(data['vwap'], d=10)
    # 2. 计算 jump_decay(ts_std_dev(vwap, 10), d=5, sensitivity=0.1, force=0.05)
    data_jump_decay = jump_decay(data_ts_std_dev, d=5, sensitivity=0.1, force=0.05)
    # 3. 计算 ts_mean(vol, 10)
    data_ts_mean = ts_mean(data['vol'], d=10)
    # 4. 计算 divide(jump_decay(ts_std_dev(vwap, 10), d=5, sensitivity=0.1, force=0.05), ts_mean(vol, 10))
    factor = divide(data_jump_decay, data_ts_mean)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()