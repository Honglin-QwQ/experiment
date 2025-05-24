import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_std_dev, ts_delta

def factor_5694(data, **kwargs):
    """
    因子名称: Volatility_Trend_Divergence_19174
    数学表达式: ts_corr(ts_std_dev(low, 13), ts_delta(high, 5), 21)
    中文描述: 该因子计算了最低价的短期波动率（基于过去13天的标准差）与最高价的短期变化（基于过去5天的差值）在更长周期（过去21天）内的相关性。它旨在捕捉市场在低位时的波动性变化趋势与高位时的价格动量变化趋势之间的背离或一致性。当低位波动率上升而高位价格变化趋缓，或者反之，可能预示着市场情绪或趋势的潜在变化。这结合了参考因子中对低价波动率的关注和对高价变化率的分析，通过引入相关性分析，增加了因子的创新性和复杂性，用于识别市场动量和风险之间的动态关系。
    因子应用场景：
    1. 市场情绪反转识别：当因子值出现极端值时，可能预示着市场情绪即将发生反转。
    2. 趋势确认：因子值持续上升或下降可能确认当前趋势的强度。
    3. 风险评估：通过观察低位波动率和高位价格变化的相关性，评估市场风险水平。
    """
    # 1. 计算 ts_std_dev(low, 13)
    data_ts_std_dev_low = ts_std_dev(data['low'], 13)
    # 2. 计算 ts_delta(high, 5)
    data_ts_delta_high = ts_delta(data['high'], 5)
    # 3. 计算 ts_corr(ts_std_dev(low, 13), ts_delta(high, 5), 21)
    factor = ts_corr(data_ts_std_dev_low, data_ts_delta_high, 21)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()