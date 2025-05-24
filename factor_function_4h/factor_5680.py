import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, divide, ts_delta, ts_delay

def factor_5680(data, **kwargs):
    """
    因子名称: factor_0002_69388
    数学表达式: ts_std_dev(divide(ts_delta(close, 1), ts_delay(vol, 1)), 5)
    中文描述: 该因子计算过去5天内，每日收盘价变化与前一日成交量的比值的标准差。其核心思想是结合价格变化和成交量变化来衡量市场的波动性。具体来说，首先计算每日收盘价的变化（ts_delta(close, 1)），然后将其除以前一日的成交量（ts_delay(vol, 1)），得到一个量价结合的指标，最后计算这个指标在过去5天内的标准差。创新点在于将价格变化与成交量进行结合，从而更全面地反映市场的波动性和交易活跃度。
    因子应用场景：
    1. 波动性衡量：用于衡量市场或特定股票的波动性。
    2. 交易活跃度评估：结合成交量变化，评估市场的交易活跃程度。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 2. 计算 ts_delay(vol, 1)
    data_ts_delay_vol = ts_delay(data['vol'], 1)
    # 3. 计算 divide(ts_delta(close, 1), ts_delay(vol, 1))
    data_divide = divide(data_ts_delta_close, data_ts_delay_vol)
    # 4. 计算 ts_std_dev(divide(ts_delta(close, 1), ts_delay(vol, 1)), 5)
    factor = ts_std_dev(data_divide, 5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()