import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_zscore, ts_delta, multiply

def factor_6092(data, **kwargs):
    """
    数学表达式: ts_corr(ts_zscore(ts_delta(low, 3), 22), ts_zscore(multiply(ts_delta(close, 3), vol), 22), 10)
    中文描述: 该因子在参考因子的基础上进行了创新。它首先计算最低价3日变化的22日Z分数标准化，这部分与参考因子类似，用于衡量低价动量。创新点在于第二个序列的构建：它计算收盘价3日变化与当日成交量的乘积，并对这个乘积进行22日Z分数标准化。这个乘积项结合了价格变化和成交量信息，旨在捕捉在有成交量支持下的价格动量。最后，因子计算这两个标准化序列在过去10天的相关性。通过引入成交量加权的收盘价变化，该因子试图识别低价动量与有成交量支持的价格动量之间的关系，这可能有助于区分由真实交易活动驱动的价格变化和噪音，从而提升因子的预测能力和稳定性。
    因子应用场景：
    1. 量价关系分析：该因子可以用于分析低价动量与成交量加权的价格动量之间的关系，帮助识别由真实交易活动驱动的价格变化。
    2. 趋势确认：当因子值较高时，可能表明低价上涨趋势得到成交量的有效支持，从而增强趋势的可信度。
    3. 市场情绪判断：通过观察因子值的变化，可以辅助判断市场情绪，例如，因子值持续上升可能反映市场对低价股的乐观情绪。
    """
    # 1. 计算 ts_delta(low, 3)
    data_ts_delta_low = ts_delta(data['low'], 3)
    # 2. 计算 ts_zscore(ts_delta(low, 3), 22)
    data_ts_zscore_low = ts_zscore(data_ts_delta_low, 22)
    # 3. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], 3)
    # 4. 计算 multiply(ts_delta(close, 3), vol)
    data_multiply_close_vol = multiply(data_ts_delta_close, data['vol'])
    # 5. 计算 ts_zscore(multiply(ts_delta(close, 3), vol), 22)
    data_ts_zscore_close_vol = ts_zscore(data_multiply_close_vol, 22)
    # 6. 计算 ts_corr(ts_zscore(ts_delta(low, 3), 22), ts_zscore(multiply(ts_delta(close, 3), vol), 22), 10)
    factor = ts_corr(data_ts_zscore_low, data_ts_zscore_close_vol, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()