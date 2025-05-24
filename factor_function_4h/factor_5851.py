import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_skewness, ts_std_dev, multiply

def factor_5851(data, **kwargs):
    """
    因子名称: VolPriceRatio_VolatilitySkew_52699
    数学表达式: divide(ts_skewness(divide(close, vol), 90), ts_std_dev(multiply(vol, close), 90))
    中文描述: 该因子旨在捕捉价量关系波动性的偏度和成交额波动性的标准差之间的关系。首先，计算每日收盘价除以交易量的比值，并在过去90天内计算其偏度（ts_skewness）。同时，计算每日交易量与收盘价的乘积（成交额），并在过去90天内计算其标准差（ts_std_dev）。最后，将价格与交易量比率的偏度除以成交额的标准差。这个比率可以反映价格与交易量比率分布的非对称性相对于成交额波动性的程度。高值可能表明在过去一段时间内，单位交易量价格的分布呈现明显的偏态（例如，极端高或低的单位交易量价格出现的频率不对称），而成交额的波动相对稳定。该因子创新性地结合了偏度和标准差这两种统计量，并应用于不同的价量组合，以捕捉市场中更复杂的波动模式。参考了历史输出中对波动性的关注，并引入了偏度这一新的统计特征，同时根据改进建议调整了时间窗口并简化了表达式的组合方式。
    因子应用场景：
    1. 波动性分析：用于识别价格与交易量比率的偏度相对于成交额波动性的程度。
    2. 市场异常检测：高值可能表明市场存在异常波动或非对称性。
    3. 量化交易：结合其他因子，用于构建更复杂的交易策略。
    """
    # 1. 计算 divide(close, vol)
    data_divide_close_vol = divide(data['close'], data['vol'])
    # 2. 计算 ts_skewness(divide(close, vol), 90)
    data_ts_skewness = ts_skewness(data_divide_close_vol, d=90)
    # 3. 计算 multiply(vol, close)
    data_multiply_vol_close = multiply(data['vol'], data['close'])
    # 4. 计算 ts_std_dev(multiply(vol, close), 90)
    data_ts_std_dev = ts_std_dev(data_multiply_vol_close, d=90)
    # 5. 计算 divide(ts_skewness(divide(close, vol), 90), ts_std_dev(multiply(vol, close), 90))
    factor = divide(data_ts_skewness, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()