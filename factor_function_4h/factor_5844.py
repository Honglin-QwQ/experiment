import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_entropy, ts_std_dev, subtract, add

def factor_5844(data, **kwargs):
    """
    数学表达式: divide(ts_entropy(vwap, 106), ts_std_dev(divide(subtract(close, open), add(subtract(high, low), 0.001)), 106))
    中文描述: 该因子计算了VWAP在过去106天的信息熵与当日价格波动强度（收盘价减开盘价除以日内振幅）在过去106天的标准差之比。VWAP熵衡量了VWAP的不确定性或混乱度，而价格波动强度的标准差衡量了日内价格波动模式的稳定性。该因子通过结合两个参考因子中的元素（VWAP熵和基于开盘价、收盘价、最高价、最低价的价格波动强度），创造性地构建了一个衡量市场不确定性相对于日内波动模式稳定性的指标。较高的因子值可能表明市场在VWAP层面存在较高的不确定性，但日内波动模式相对稳定，这可能预示着潜在的价格突破或趋势形成；较低的因子值则可能表明VWAP相对稳定，而日内波动模式不稳定，市场缺乏明确方向。该因子可用于识别市场情绪和波动模式的变化，辅助交易策略的制定。
    因子应用场景：
    1. 市场不确定性评估：用于评估市场在VWAP层面的不确定性与日内价格波动模式稳定性之间的关系。
    2. 波动模式识别：识别日内波动模式的变化，辅助判断市场方向。
    3. 交易策略制定：辅助制定基于市场情绪和波动模式变化的交易策略。
    """
    # 1. 计算 ts_entropy(vwap, 106)
    data_ts_entropy_vwap = ts_entropy(data['vwap'], 106)
    # 2. 计算 subtract(close, open)
    data_subtract_close_open = subtract(data['close'], data['open'])
    # 3. 计算 subtract(high, low)
    data_subtract_high_low = subtract(data['high'], data['low'])
    # 4. 计算 add(subtract(high, low), 0.001)
    data_add_subtract_high_low = add(data_subtract_high_low, 0.001)
    # 5. 计算 divide(subtract(close, open), add(subtract(high, low), 0.001))
    data_divide_subtract_close_open = divide(data_subtract_close_open, data_add_subtract_high_low)
    # 6. 计算 ts_std_dev(divide(subtract(close, open), add(subtract(high, low), 0.001)), 106)
    data_ts_std_dev_divide_subtract_close_open = ts_std_dev(data_divide_subtract_close_open, 106)
    # 7. 计算 divide(ts_entropy(vwap, 106), ts_std_dev(divide(subtract(close, open), add(subtract(high, low), 0.001)), 106))
    factor = divide(data_ts_entropy_vwap, data_ts_std_dev_divide_subtract_close_open)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()