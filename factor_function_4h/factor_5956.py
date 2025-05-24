import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_std_dev, abs, subtract, ts_max, ts_delay, divide

def factor_5956(data, **kwargs):
    """
    因子名称: Volatility_Jump_Momentum_Ratio_75469
    数学表达式: divide(ts_std_dev(close, 30), abs(subtract(ts_max(open, 60), ts_delay(open, 1))))
    中文描述: 该因子计算了过去30天收盘价的标准差与过去60天开盘价最大值和昨日开盘价差值的绝对值的比率。标准差衡量了短期价格波动性，而分母则捕捉了开盘价相对于近期高点的“跳跃”或“回撤”幅度。通过这个比率，我们可以评估短期波动相对于近期开盘价大幅变动的强度。较高的比率可能表明在开盘价经历大幅变动后，短期波动正在加剧，可能预示着潜在的趋势反转或持续动量；较低的比率则可能意味着价格波动相对稳定，近期开盘价的变动并未引发剧烈的短期波动。这是一个结合短期波动和近期开盘价“跳跃”的创新性因子，旨在识别潜在的动量信号和风险水平。相较于参考因子，分母的计算更加关注最近一次开盘价与过去一段时间最高开盘价的差异，而非简单的时间序列最大差值，这可能更能捕捉到近期的市场情绪变化。
    因子应用场景：
    1. 动量信号识别：用于识别短期波动相对于近期开盘价大幅变动的强度，辅助判断潜在的动量信号。
    2. 风险评估：评估短期波动相对于开盘价跳跃的程度，辅助判断市场风险水平。
    """
    # 1. 计算 ts_std_dev(close, 30)
    data_ts_std_dev = ts_std_dev(data['close'], 30)
    # 2. 计算 ts_max(open, 60)
    data_ts_max = ts_max(data['open'], 60)
    # 3. 计算 ts_delay(open, 1)
    data_ts_delay = ts_delay(data['open'], 1)
    # 4. 计算 subtract(ts_max(open, 60), ts_delay(open, 1))
    data_subtract = subtract(data_ts_max, data_ts_delay)
    # 5. 计算 abs(subtract(ts_max(open, 60), ts_delay(open, 1)))
    data_abs = abs(data_subtract)
    # 6. 计算 divide(ts_std_dev(close, 30), abs(subtract(ts_max(open, 60), ts_delay(open, 1))))
    factor = divide(data_ts_std_dev, data_abs)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()