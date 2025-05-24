import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_entropy, ts_delay, divide, rank

def factor_6105(data, **kwargs):
    """
    数学表达式: rank(divide(ts_entropy(vol, 90) - ts_delay(ts_entropy(vol, 90), 2), ts_entropy(ts_delay(vol, 2), 90)))
    中文描述: 该因子计算当前成交量在过去90天时间序列中的信息熵与两日前信息熵的差值，再除以两日前信息熵，最后计算其在截面上的排名。这是一个创新性的因子，结合了信息论的概念和时间序列分析，旨在捕捉成交量模式变化的相对幅度，并通过排名来消除不同股票之间的绝对差异。相较于原始因子，该因子调整了时间窗口和延迟期，并引入了排名操作，可能更有效地识别市场活跃度和结构变化的相对强度，用于识别潜在的交易机会或风险。
    因子应用场景：
    1. 市场活跃度识别：因子值较高可能表明市场对该股票的关注度增加，成交量模式变化剧烈。
    2. 结构变化检测：通过信息熵的变化，可以检测成交量分布的结构性变化，例如由稳定到分散或由分散到集中的转变。
    3. 交易机会发现：因子可以辅助识别成交量异常变化的股票，这些股票可能存在潜在的交易机会。
    """
    # 1. 计算 ts_entropy(vol, 90)
    data_ts_entropy = ts_entropy(data['vol'], 90)
    # 2. 计算 ts_delay(vol, 2)
    data_ts_delay_vol = ts_delay(data['vol'], 2)
    # 3. 计算 ts_entropy(ts_delay(vol, 2), 90)
    data_ts_entropy_delay = ts_entropy(data_ts_delay_vol, 90)
    # 4. 计算 ts_delay(ts_entropy(vol, 90), 2)
    data_ts_delay_entropy = ts_delay(data_ts_entropy, 2)
    # 5. 计算 ts_entropy(vol, 90) - ts_delay(ts_entropy(vol, 90), 2)
    data_subtract = data_ts_entropy - data_ts_delay_entropy
    # 6. 计算 divide(ts_entropy(vol, 90) - ts_delay(ts_entropy(vol, 90), 2), ts_entropy(ts_delay(vol, 2), 90))
    data_divide = divide(data_subtract, data_ts_entropy_delay)
    # 7. 计算 rank(divide(ts_entropy(vol, 90) - ts_delay(ts_entropy(vol, 90), 2), ts_entropy(ts_delay(vol, 2), 90)))
    factor = rank(data_divide, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()