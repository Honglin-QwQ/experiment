import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, multiply, ts_skewness, ts_delta

def factor_5976(data, **kwargs):
    """
    因子名称: VolSkewPriceChangeDecay_69417
    数学表达式: ts_decay_exp_window(multiply(ts_skewness(vol, 5), ts_delta(close, 2)), 10, factor = 0.6)
    中文描述: 该因子首先计算过去5天成交量的偏度，衡量成交量分布的非对称性。然后计算收盘价的2日变化，捕捉短期价格动量。将这两者相乘，得到一个结合了短期量价特征的指标。最后，使用指数衰减加权平均计算这个乘积在过去10天的值，并设置衰减因子为0.6，使得近期的数据具有更高的权重。正偏度可能表示近期成交量中存在极端高值，而负偏度表示存在极端低值。结合价格变化，这个因子试图捕捉由非对称成交量模式驱动的、具有衰减效应的短期价格趋势。相较于参考因子，创新点在于结合了成交量的偏度而非直接成交量，并引入了指数衰减加权平均来反映近期数据的重要性，同时调整了时间窗口和衰减因子以优化因子表现。这可以用于识别短期内由市场情绪和交易活动非对称性驱动的、具有一定持续性的价格变化。
    因子应用场景：
    1. 短期趋势识别：捕捉由成交量偏度和价格变化共同驱动的短期趋势。
    2. 市场情绪分析：通过成交量偏度反映市场情绪，并结合价格变化预测短期价格走势。
    """
    # 1. 计算 ts_skewness(vol, 5)
    data_ts_skewness_vol = ts_skewness(data['vol'], 5)
    # 2. 计算 ts_delta(close, 2)
    data_ts_delta_close = ts_delta(data['close'], 2)
    # 3. 计算 multiply(ts_skewness(vol, 5), ts_delta(close, 2))
    data_multiply = multiply(data_ts_skewness_vol, data_ts_delta_close)
    # 4. 计算 ts_decay_exp_window(multiply(ts_skewness(vol, 5), ts_delta(close, 2)), 10, factor = 0.6)
    factor = ts_decay_exp_window(data_multiply, 10, factor = 0.6)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()