import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_skewness, ts_mean, ts_delta, divide

def factor_5918(data, **kwargs):
    """
    因子名称: VolatilitySkewMomentumRatio_49243
    数学表达式: divide(ts_skewness(close, 30), ts_mean(ts_delta(close, 10), 15))
    中文描述: 该因子计算了收盘价在过去30天的偏度与收盘价在过去10天变动量的过去15天均值之比。偏度衡量了价格分布的非对称性，反映了极端价格变动的可能性，而变动量的均值则反映了价格的中期动量。通过比较价格分布的偏度和中期动量，该因子试图识别在不同市场环境下，价格变动是否伴随着非对称的风险或机会。创新点在于引入了偏度这一统计量来捕捉价格分布的特性，并将其与中期动量相结合，使用比率形式来捕捉它们之间的相对关系，可能用于识别潜在的尾部风险或机会。
    因子应用场景：
    1. 风险识别：用于识别市场中存在的潜在尾部风险。
    2. 机会识别：用于发现价格变动伴随着非对称机会的市场环境。
    3. 市场环境分析：帮助理解市场价格分布的特性和中期动量。
    """
    # 1. 计算 ts_skewness(close, 30)
    data_ts_skewness = ts_skewness(data['close'], 30)
    # 2. 计算 ts_delta(close, 10)
    data_ts_delta = ts_delta(data['close'], 10)
    # 3. 计算 ts_mean(ts_delta(close, 10), 15)
    data_ts_mean = ts_mean(data_ts_delta, 15)
    # 4. 计算 divide(ts_skewness(close, 30), ts_mean(ts_delta(close, 10), 15))
    factor = divide(data_ts_skewness, data_ts_mean)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()