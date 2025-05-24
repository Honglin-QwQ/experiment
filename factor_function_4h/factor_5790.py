import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_decay_linear, ts_delta

def factor_5790(data, **kwargs):
    """
    因子名称: Vol_Price_Trend_Correlation_Decay_42436
    数学表达式: ts_corr(ts_decay_linear(ts_delta(vol, 1), 5), ts_decay_linear(ts_delta(close, 1), 5), 10)
    中文描述: 该因子计算过去5天成交量变化和收盘价变化的线性衰减值，然后计算这两个衰减序列在过去10天内的相关性。通过使用ts_decay_linear对量价变化进行衰减处理，可以赋予近期变化更大的权重，从而更敏感地捕捉短期量价趋势的一致性。这种方法相较于直接计算量价变化的相关性，更能反映近期市场行为对未来趋势的影响。该因子可以用于识别量价配合的强度和方向，辅助判断趋势的持续性或潜在反转，特别适用于关注短期市场动态的交易策略。
    因子应用场景：
    1. 量价关系识别：用于识别量价配合的强度和方向，辅助判断趋势的持续性或潜在反转。
    2. 短期市场动态：特别适用于关注短期市场动态的交易策略。
    """
    # 1. 计算 ts_delta(vol, 1)
    data_ts_delta_vol = ts_delta(data['vol'], 1)
    # 2. 计算 ts_decay_linear(ts_delta(vol, 1), 5)
    data_ts_decay_linear_vol = ts_decay_linear(data_ts_delta_vol, 5)
    del data_ts_delta_vol

    # 3. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 4. 计算 ts_decay_linear(ts_delta(close, 1), 5)
    data_ts_decay_linear_close = ts_decay_linear(data_ts_delta_close, 5)
    del data_ts_delta_close

    # 5. 计算 ts_corr(ts_decay_linear(ts_delta(vol, 1), 5), ts_decay_linear(ts_delta(close, 1), 5), 10)
    factor = ts_corr(data_ts_decay_linear_vol, data_ts_decay_linear_close, 10)
    del data_ts_decay_linear_vol
    del data_ts_decay_linear_close

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()