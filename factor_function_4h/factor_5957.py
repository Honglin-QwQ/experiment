import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_decay_linear, ts_std_dev, adv

def factor_5957(data, **kwargs):
    """
    数学表达式: ts_corr(ts_decay_linear(vol, 60), ts_std_dev(adv(vol, 20), 120), 90)
    中文描述: 该因子旨在捕捉经过线性衰减加权的成交量与长期平均成交量波动性之间的相关性。它首先计算过去60天内成交量的线性衰减加权平均值，赋予近期成交量更高的权重。然后计算过去120天平均成交量的标准差，衡量长期成交量的波动性。最后，计算这两者在过去90天内的相关性。高相关性可能表明近期成交量的趋势与长期成交量的波动性同步，这可能预示着市场情绪和流动性的变化。相较于参考因子，该因子的创新点在于使用了线性衰减来处理近期成交量，赋予近期的成交量变化更大的权重，同时结合了长期平均成交量的波动性，并通过时间序列相关性来衡量它们之间的动态关系，以期更有效地捕捉市场信号。此外，该因子也借鉴了参考因子中对成交量均值和标准差的使用，但通过不同的组合方式和时间窗口进行了创新。
    因子应用场景：
    1. 市场情绪分析：用于识别成交量变化与长期波动性之间的关系，辅助判断市场情绪。
    2. 流动性预警：通过监测成交量和波动性的相关性，预警市场流动性风险。
    3. 趋势确认：验证成交量趋势与长期波动性是否一致，辅助确认市场趋势的可靠性。
    """
    # 1. 计算 ts_decay_linear(vol, 60)
    data_ts_decay_linear_vol = ts_decay_linear(data['vol'], d = 60)
    # 2. 计算 adv(vol, 20)
    data_adv_vol = adv(data['vol'], d = 20)
    # 3. 计算 ts_std_dev(adv(vol, 20), 120)
    data_ts_std_dev_adv_vol = ts_std_dev(data_adv_vol, d = 120)
    # 4. 计算 ts_corr(ts_decay_linear(vol, 60), ts_std_dev(adv(vol, 20), 120), 90)
    factor = ts_corr(data_ts_decay_linear_vol, data_ts_std_dev_adv_vol, d = 90)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()