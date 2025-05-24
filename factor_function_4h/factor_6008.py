import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, multiply, divide

def factor_6008(data, **kwargs):
    """
    因子名称: VolumeWeightedLowCloseStdDevRatio_99110
    数学表达式: divide(ts_std_dev(multiply(low, vol), 20), ts_std_dev(multiply(close, vol), 60))
    中文描述: 该因子计算了短期（20天）成交量加权最低价的标准差与长期（60天）成交量加权收盘价的标准差之比。参考了历史因子的标准差计算和时间窗口差异。
            创新的地方在于：1. 引入了成交量对价格的加权，以反映市场活跃度对价格波动的影响。
                        2. 比较了不同时间窗口下，成交量加权的最低价和收盘价的波动性差异。
                        3. 使用divide操作符计算比值，以捕捉短期成交量加权最低价波动性相对于长期成交量加权收盘价波动性的相对强弱。
                        高值可能预示着近期低价在活跃交易下的波动性增强，而收盘价的长期波动性相对稳定；低值则相反。这可以用于识别价格波动的结构性变化。
    因子应用场景：
    1. 波动性分析：用于衡量短期低价波动相对于长期收盘价波动的强度。
    2. 趋势识别：高值可能预示着下跌趋势中的活跃交易，低值可能预示着上涨趋势中的稳定交易。
    """
    # 1. 计算 multiply(low, vol)
    data_multiply_low_vol = multiply(data['low'], data['vol'])
    # 2. 计算 ts_std_dev(multiply(low, vol), 20)
    data_ts_std_dev_low_vol = ts_std_dev(data_multiply_low_vol, d = 20)
    # 3. 计算 multiply(close, vol)
    data_multiply_close_vol = multiply(data['close'], data['vol'])
    # 4. 计算 ts_std_dev(multiply(close, vol), 60)
    data_ts_std_dev_close_vol = ts_std_dev(data_multiply_close_vol, d = 60)
    # 5. 计算 divide(ts_std_dev(multiply(low, vol), 20), ts_std_dev(multiply(close, vol), 60))
    factor = divide(data_ts_std_dev_low_vol, data_ts_std_dev_close_vol)

    # 删除中间变量
    del data_multiply_low_vol
    del data_ts_std_dev_low_vol
    del data_multiply_close_vol
    del data_ts_std_dev_close_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()