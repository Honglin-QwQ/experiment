import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_std_dev, divide, ts_mean, ts_corr

def factor_5840(data, **kwargs):
    """
    因子名称: Volume_Price_Volatility_Correlation_71418
    数学表达式: rank(ts_std_dev(divide(volume, ts_mean(volume, 20)), 60)) - rank(ts_corr(close, ts_mean(close, 20), 60))
    中文描述: 该因子旨在捕捉成交量相对波动性与收盘价及其长期均线相关性之间的关系。首先，计算过去60天内相对成交量（当前成交量除以过去20天平均成交量）的标准差，并对其进行排名。高排名表示相对成交量波动剧烈，可能预示着市场情绪的变化。其次，计算收盘价与过去20天平均收盘价在过去60天内的相关性，并对其进行排名。收盘价与其长期均线的相关性反映了价格趋势的强度和持续性。最后，用相对成交量标准差的排名减去价格相关性的排名。当相对成交量波动剧烈且收盘价与其长期均线的相关性较低时，因子值较高，可能指示着趋势的潜在反转或动量减弱。创新点在于使用了相对成交量的波动性，并结合了收盘价与其长期均线的相关性，从成交量和价格趋势两个维度进行分析，并使用排名进行标准化处理，增强了可比性。相较于历史输出，该因子移除了`inverse(vwap)`部分，并替换为收盘价与其长期均线的相关性，以解决历史输出中`inverse(vwap)`可能引入的噪音和负相关问题。同时，将成交量变化替换为相对成交量，以更好地衡量成交量的异常波动。
    因子应用场景：
    1. 趋势反转识别：当因子值较高时，可能指示着趋势的潜在反转或动量减弱。
    2. 市场情绪分析：通过成交量和价格趋势的结合，辅助判断市场情绪。
    """
    # 1. 计算 ts_mean(volume, 20)
    volume_mean_20 = ts_mean(data['vol'], d = 20)
    # 2. 计算 divide(volume, ts_mean(volume, 20))
    relative_volume = divide(data['vol'], volume_mean_20)
    # 3. 计算 ts_std_dev(divide(volume, ts_mean(volume, 20)), 60)
    volume_volatility = ts_std_dev(relative_volume, d = 60)
    # 4. 计算 rank(ts_std_dev(divide(volume, ts_mean(volume, 20)), 60))
    volume_volatility_rank = rank(volume_volatility, rate = 2)
    # 5. 计算 ts_mean(close, 20)
    close_mean_20 = ts_mean(data['close'], d = 20)
    # 6. 计算 ts_corr(close, ts_mean(close, 20), 60)
    price_correlation = ts_corr(data['close'], close_mean_20, d = 60)
    # 7. 计算 rank(ts_corr(close, ts_mean(close, 20), 60))
    price_correlation_rank = rank(price_correlation, rate = 2)
    # 8. 计算 rank(ts_std_dev(divide(volume, ts_mean(volume, 20)), 60)) - rank(ts_corr(close, ts_mean(close, 20), 60))
    factor = volume_volatility_rank - price_correlation_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()