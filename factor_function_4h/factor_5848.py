import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_std_dev, divide, adv, ts_decay_linear

def factor_5848(data, **kwargs):
    """
    因子名称: Volume_Volatility_Price_Decay_Diff_94541
    数学表达式: rank(ts_std_dev(divide(volume, adv(volume, 20)), 60)) - rank(ts_decay_linear(close, 60))
    中文描述: 该因子旨在捕捉相对成交量波动性与收盘价线性衰减平均值之间的差异排名。首先，计算过去60天内相对成交量（当前成交量除以过去20天平均成交量）的标准差，并对其进行排名。高排名表示相对成交量波动剧烈，可能预示着市场情绪的变化。其次，计算过去60天内收盘价的线性衰减平均值，并对其进行排名。线性衰减平均值赋予近期收盘价更高的权重，反映了近期价格趋势。最后，用相对成交量标准差的排名减去收盘价线性衰减平均值的排名。当相对成交量波动剧烈且近期收盘价线性衰减平均值排名较低时，因子值较高，可能指示着趋势的潜在反转或动量减弱。创新点在于使用了相对成交量的波动性，并结合了收盘价的线性衰减平均值，从成交量和价格趋势两个维度进行分析，并使用排名进行标准化处理，增强了可比性。相较于历史输出，该因子移除了`ts_corr`部分，并替换为收盘价的线性衰减平均值，以解决历史输出中相关性可能引入的噪音和负相关问题。同时，将成交量变化替换为相对成交量，以更好地衡量成交量的异常波动，并根据评估报告的建议，尝试使用`ts_decay_linear`操作符来捕捉价格的近期趋势。
    因子应用场景：
    1. 趋势反转识别：因子值较高可能指示着趋势的潜在反转或动量减弱。
    2. 市场情绪分析：相对成交量波动剧烈可能预示着市场情绪的变化。
    """
    # 1. 计算 adv(volume, 20)
    data_adv_volume = adv(data['vol'], d = 20)
    # 2. 计算 divide(volume, adv(volume, 20))
    data_divide_volume_adv = divide(data['vol'], data_adv_volume)
    # 3. 计算 ts_std_dev(divide(volume, adv(volume, 20)), 60)
    data_ts_std_dev = ts_std_dev(data_divide_volume_adv, d = 60)
    # 4. 计算 rank(ts_std_dev(divide(volume, adv(volume, 20)), 60))
    data_rank_ts_std_dev = rank(data_ts_std_dev, rate = 2)
    # 5. 计算 ts_decay_linear(close, 60)
    data_ts_decay_linear = ts_decay_linear(data['close'], d = 60)
    # 6. 计算 rank(ts_decay_linear(close, 60))
    data_rank_ts_decay_linear = rank(data_ts_decay_linear, rate = 2)
    # 7. 计算 rank(ts_std_dev(divide(volume, adv(volume, 20)), 60)) - rank(ts_decay_linear(close, 60))
    factor = data_rank_ts_std_dev - data_rank_ts_decay_linear

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()