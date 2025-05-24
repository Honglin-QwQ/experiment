import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_sum, multiply, divide, subtract, ts_delay, ts_std_dev

def factor_5797(data, **kwargs):
    """
    因子名称: Volatility_Weighted_Volume_Flow_Index_67400
    数学表达式: ts_sum(multiply(divide(subtract(close, ts_delay(close, 1)), ts_std_dev(close, 10)), divide(subtract(vol, ts_delay(vol, 1)), ts_std_dev(vol, 10))), 15)
    中文描述: 该因子旨在捕捉价格波动和成交量变化之间的相互作用，并将其累积以衡量潜在的资金流向。它首先计算每日收盘价变化和成交量变化的标准化值（通过除以各自的10日标准差），然后将这两个标准化值相乘。最后，对乘积进行15天的累积求和。标准化处理使得不同量级的价格和成交量变化具有可比性；乘法则放大了价格和成交量同向变动（例如，价格上涨伴随成交量增加）的影响；累积求和则反映了这种相互作用在一段时间内的持续性和强度。该因子创新性地结合了价格波动率和成交量波动率，并以乘积形式捕捉它们的协同效应，累积结果可用于识别市场情绪的潜在变化和资金的流入/流出压力。
    因子应用场景：
    1. 趋势识别：识别市场情绪的潜在变化和资金的流入/流出压力。
    2. 资金流向：衡量潜在的资金流向。
    """
    # 1. 计算 ts_delay(close, 1)
    close_delayed = ts_delay(data['close'], d=1)
    # 2. 计算 subtract(close, ts_delay(close, 1))
    close_diff = subtract(data['close'], close_delayed)
    # 3. 计算 ts_std_dev(close, 10)
    close_std = ts_std_dev(data['close'], d=10)
    # 4. 计算 divide(subtract(close, ts_delay(close, 1)), ts_std_dev(close, 10))
    close_normalized = divide(close_diff, close_std)

    # 5. 计算 ts_delay(vol, 1)
    vol_delayed = ts_delay(data['vol'], d=1)
    # 6. 计算 subtract(vol, ts_delay(vol, 1))
    vol_diff = subtract(data['vol'], vol_delayed)
    # 7. 计算 ts_std_dev(vol, 10)
    vol_std = ts_std_dev(data['vol'], d=10)
    # 8. 计算 divide(subtract(vol, ts_delay(vol, 1)), ts_std_dev(vol, 10))
    vol_normalized = divide(vol_diff, vol_std)

    # 9. 计算 multiply(divide(subtract(close, ts_delay(close, 1)), ts_std_dev(close, 10)), divide(subtract(vol, ts_delay(vol, 1)), ts_std_dev(vol, 10)))
    multiplied = multiply(close_normalized, vol_normalized)
    # 10. 计算 ts_sum(multiply(divide(subtract(close, ts_delay(close, 1)), ts_std_dev(close, 10)), divide(subtract(vol, ts_delay(vol, 1)), ts_std_dev(vol, 10))), 15)
    factor = ts_sum(multiplied, d=15)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()