import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_delta, ts_std_dev, adv

def factor_5667(data, **kwargs):
    """
    因子名称: factor_volatility_adjusted_momentum_75083
    数学表达式: ts_corr(ts_delta(close, 5), ts_std_dev(close, 10) / adv(20), 10)
    中文描述: 本因子旨在捕捉价格动量与波动率调整后的成交量之间的关系。它首先计算收盘价的5日差分（ts_delta(close, 5)），以此衡量短期价格动量。同时，计算收盘价的10日标准差（ts_std_dev(close, 10)），并除以20日平均成交量（adv(20)）进行标准化，以反映波动率调整后的市场活跃度。最后，计算这两个时间序列在过去10天的相关性（ts_corr(..., 10)），用于识别价格动量与波动率调整后成交量之间的关系。创新之处在于将波动率与成交量结合，更准确地反映市场情绪，并以此判断动量和波动之间的关系，可能用于识别趋势的持续性或反转。
    因子应用场景：
    1. 趋势识别：识别价格动量与波动率调整后成交量之间的关系，可能用于识别趋势的持续性或反转。
    2. 市场情绪分析：通过波动率与成交量的结合，更准确地反映市场情绪。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 2. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], 10)
    # 3. 计算 adv(20)
    data_adv = adv(data['vol'], 20)
    # 4. 计算 ts_std_dev(close, 10) / adv(20)
    data_divide = data_ts_std_dev_close / data_adv
    # 5. 计算 ts_corr(ts_delta(close, 5), ts_std_dev(close, 10) / adv(20), 10)
    factor = ts_corr(data_ts_delta_close, data_divide, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()