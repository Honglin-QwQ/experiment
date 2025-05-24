import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5912(data, **kwargs):
    """
    因子名称: VolEntropyPriceChangeRatio_13377
    数学表达式: divide(ts_entropy(vol, 90), abs(ts_delta(close, 10)))
    中文描述: 该因子计算了过去90天成交量的时间序列熵与过去10天收盘价绝对变化的比例。成交量时间序列熵衡量了成交量分布的不确定性，较高的熵值意味着成交量波动较大，市场活跃度或情绪变化剧烈。收盘价绝对变化则衡量了价格在短期内的变动幅度。将成交量熵除以收盘价绝对变化，旨在捕捉在价格变动幅度不同的情况下，成交量不确定性的相对强度。较高的比值可能表明在价格波动相对较小的情况下，成交量却显示出较高的不确定性，这可能预示着潜在的市场情绪变化或资金流向的异动。相较于参考因子，创新点在于：1. 扩大了成交量熵的计算窗口至90天，以捕捉更长期的成交量不确定性趋势；2. 将分母从价格标准差改为短期（10天）收盘价的绝对变化，更直接地衡量价格的短期动量；3. 使用绝对变化而非标准差，避免了标准差对极端值的敏感性，更关注价格的实际变动幅度。改进建议的采纳体现在：1. 调整了时间窗口参数，将成交量熵窗口扩大到90天，价格变化窗口缩小到10天，以期捕捉不同时间尺度的市场特征；2. 调整了分母，使用短期价格的绝对变化代替标准差，引入了更直接的价格方向信息（通过绝对值）。
    因子应用场景：
    1. 市场情绪分析：用于识别在价格变动不大的情况下成交量波动较大的股票，可能预示着市场情绪的潜在变化。
    2. 资金流向监控：较高的因子值可能表明资金流向的异动，例如在价格稳定时成交量熵增加，可能意味着资金正在暗中布局或撤离。
    3. 风险预警：当因子值异常升高时，可能预示着市场风险的增加，例如成交量的不确定性增加可能导致价格波动加剧。
    """
    # 1. 计算 ts_entropy(vol, 90)
    data_ts_entropy_vol = ts_entropy(data['vol'], 90)
    # 2. 计算 ts_delta(close, 10)
    data_ts_delta_close = ts_delta(data['close'], 10)
    # 3. 计算 abs(ts_delta(close, 10))
    data_abs_ts_delta_close = abs(data_ts_delta_close)
    # 4. 计算 divide(ts_entropy(vol, 90), abs(ts_delta(close, 10)))
    factor = divide(data_ts_entropy_vol, data_abs_ts_delta_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()