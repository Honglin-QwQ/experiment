import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_6054(data, **kwargs):
    """
    因子名称: ATR_Volume_Oscillator_Ratio_60254
    数学表达式: divide(ts_mean(max(high - ts_delay(close, 1), abs(high - low), abs(low - ts_delay(close, 1))), 20), subtract(ts_mean(vol, 5), ts_mean(vol, 20)))
    中文描述: 该因子旨在捕捉真实波幅（ATR）与短期和长期成交量均线差异（成交量震荡指标）之间的动态关系。它使用20日的真实波幅 `ts_mean(max(high - ts_delay(close, 1), abs(high - low), abs(low - ts_delay(close, 1))), 20)` 来衡量近期价格的真实波动范围，这比简单的标准差更能反映包含跳空缺口的波动。同时，它使用5日和20日成交量均线的差值 `subtract(ts_mean(vol, 5), ts_mean(vol, 20))` 来衡量近期成交量的趋势变化，即成交量震荡指标。通过计算真实波幅与成交量震荡指标的比率，该因子试图识别在不同波动水平下，市场交易活跃度的相对强弱。高比率可能表明在价格波动剧烈时，成交量并未同步放大，这可能预示着趋势的不可持续性；低比率则可能表明在价格波动加剧时，成交量也显著放大，从而增强了当前趋势的可靠性。相较于参考因子，创新点在于：1. 使用真实波幅（ATR）作为波动率度量，更全面反映价格波动；2. 使用成交量震荡指标捕捉成交量趋势变化，而非简单的线性衰减；3. 因子结构为真实波幅与成交量趋势指标的比率，具有更强的量价互动经济意义。可以用于识别短期趋势的强度和潜在反转信号，或作为其他技术分析因子的补充。
    因子应用场景：
    1. 波动率与成交量关系的量化：识别在不同波动水平下，市场交易活跃度的相对强弱。
    2. 趋势识别：识别短期趋势的强度和潜在反转信号。
    3. 技术分析补充：作为其他技术分析因子的补充，提供量价互动视角。
    """
    # 1. 计算 ts_delay(close, 1)
    data['close_lag1'] = ts_delay(data['close'], 1)
    # 2. 计算 max(high - ts_delay(close, 1), abs(high - low), abs(low - ts_delay(close, 1)))
    data['atr_temp'] = max(data['high'] - data['close_lag1'], abs(data['high'] - data['low']), abs(data['low'] - data['close_lag1']))
    # 3. 计算 ts_mean(max(high - ts_delay(close, 1), abs(high - low), abs(low - ts_delay(close, 1))), 20)
    data['atr'] = ts_mean(data['atr_temp'], 20)
    # 4. 计算 ts_mean(vol, 5)
    data['vol_short'] = ts_mean(data['vol'], 5)
    # 5. 计算 ts_mean(vol, 20)
    data['vol_long'] = ts_mean(data['vol'], 20)
    # 6. 计算 subtract(ts_mean(vol, 5), ts_mean(vol, 20))
    data['volume_oscillator'] = subtract(data['vol_short'], data['vol_long'])
    # 7. 计算 divide(ts_mean(max(high - ts_delay(close, 1), abs(high - low), abs(low - ts_delay(close, 1))), 20), subtract(ts_mean(vol, 5), ts_mean(vol, 20)))
    factor = divide(data['atr'], data['volume_oscillator'])

    data.drop(columns=['close_lag1', 'atr_temp', 'atr', 'vol_short', 'vol_long', 'volume_oscillator'], inplace=True)
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()