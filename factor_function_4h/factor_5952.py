import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, multiply, ts_std_dev, adv, subtract, rank

def factor_5952(data, **kwargs):
    """
    因子名称: Scaled_Volume_Volatility_Skew_Diff_64763
    数学表达式: rank(subtract(ts_skewness(multiply(vol, ts_std_dev(close, 10)), 20), ts_skewness(multiply(adv(vol, 5), close), 30)))
    中文描述: 该因子衡量了两个不同时间窗口和计算逻辑下的量价相关偏度的差异，并对其进行排名。第一部分计算了过去20天成交量与收盘价10日标准差乘积的时间序列偏度，捕捉了成交活跃度与价格波动性结合的非对称特征。第二部分计算了过去30天5日平均成交量与收盘价乘积的时间序列偏度，关注了平滑后的成交量与价格结合的非对称特征。通过计算这两部分偏度的差值并进行排名，该因子试图识别在不同时间尺度和量价衡量方式下，市场情绪或交易行为非对称性的相对强弱。相较于参考因子，该因子创新性地引入了价格波动率（收盘价标准差）和不同时间窗口的平均成交量，并计算了两个偏度指标的差值，从而捕捉了更复杂的量价动态和其非对称性特征的相对变化，为识别具有特定波动模式和交易结构差异的股票提供了新的视角。这可以用于捕捉市场情绪的非对称性变化或识别潜在的价格异动。
    因子应用场景：
    1. 市场情绪分析：可用于识别市场情绪的非对称性变化。
    2. 异动捕捉：可用于识别潜在的价格异动。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], 10)
    # 2. 计算 multiply(vol, ts_std_dev(close, 10))
    data_multiply_vol_ts_std_dev_close = multiply(data['vol'], data_ts_std_dev_close)
    # 3. 计算 ts_skewness(multiply(vol, ts_std_dev(close, 10)), 20)
    data_ts_skewness_1 = ts_skewness(data_multiply_vol_ts_std_dev_close, 20)
    # 4. 计算 adv(vol, 5)
    data_adv_vol = adv(data['vol'], 5)
    # 5. 计算 multiply(adv(vol, 5), close)
    data_multiply_adv_vol_close = multiply(data_adv_vol, data['close'])
    # 6. 计算 ts_skewness(multiply(adv(vol, 5), close), 30)
    data_ts_skewness_2 = ts_skewness(data_multiply_adv_vol_close, 30)
    # 7. 计算 subtract(ts_skewness(multiply(vol, ts_std_dev(close, 10)), 20), ts_skewness(multiply(adv(vol, 5), close), 30))
    data_subtract = subtract(data_ts_skewness_1, data_ts_skewness_2)
    # 8. 计算 rank(subtract(ts_skewness(multiply(vol, ts_std_dev(close, 10)), 20), ts_skewness(multiply(adv(vol, 5), close), 30)))
    factor = rank(data_subtract, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()