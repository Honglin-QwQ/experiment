import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, signed_power, divide, ts_std_dev

def factor_5603(data, **kwargs):
    """
    数学表达式: ts_delta(signed_power(divide(high + low + open, 3), 2) - close, d = 3) * signed_power(vol, 0.5) / ts_std_dev(close, d = 20)
    中文描述: 本因子是对参考因子'(high + low)/2 - close'的创新性改进。它首先计算每日最高价、最低价和开盘价的均值，并对其平方，然后减去收盘价，再计算该差值的三日差分。此外，该因子还引入了成交量的平方根，以反映市场对价格变动的置信度，并除以过去20天收盘价的标准差，以衡量市场波动率。该因子的创新之处在于综合考虑了开盘价信息、成交量和波动率，从而更全面地捕捉市场情绪和价格变化的强度。该因子旨在识别短期内市场预期与实际收盘价之间的差异变化，并根据市场活跃度和波动程度进行调整，从而辅助判断价格趋势的潜在反转。
    因子应用场景：
    1. 市场情绪捕捉：该因子通过综合考虑开盘价、最高价、最低价和收盘价，能够更全面地捕捉市场情绪。
    2. 价格趋势反转判断：因子旨在识别短期内市场预期与实际收盘价之间的差异变化，并根据市场活跃度和波动程度进行调整，从而辅助判断价格趋势的潜在反转。
    """
    # 1. 计算 high + low + open
    sum_high_low_open = data['high'] + data['low'] + data['open']
    # 2. 计算 divide(high + low + open, 3)
    data_divide = divide(sum_high_low_open, 3)
    # 3. 计算 signed_power(divide(high + low + open, 3), 2)
    data_signed_power = signed_power(data_divide, 2)
    # 4. 计算 signed_power(divide(high + low + open, 3), 2) - close
    data_subtract = data_signed_power - data['close']
    # 5. 计算 ts_delta(signed_power(divide(high + low + open, 3), 2) - close, d = 3)
    data_ts_delta = ts_delta(data_subtract, d = 3)
    # 6. 计算 signed_power(vol, 0.5)
    data_signed_power_vol = signed_power(data['vol'], 0.5)
    # 7. 计算 ts_std_dev(close, d = 20)
    data_ts_std_dev = ts_std_dev(data['close'], d = 20)
    # 8. 计算 ts_delta(signed_power(divide(high + low + open, 3), 2) - close, d = 3) * signed_power(vol, 0.5) / ts_std_dev(close, d = 20)
    factor = data_ts_delta * data_signed_power_vol / data_ts_std_dev

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()