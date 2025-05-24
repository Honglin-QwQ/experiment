import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_min_diff, divide

def factor_5919(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(vol, 20), ts_min_diff(close, 15))
    中文描述: 该因子旨在捕捉成交量的波动性与收盘价短期支撑位之间的关系。它计算过去20天成交量的标准差，并将其除以当前收盘价与过去15天最低价的差值。高因子值可能表明在当前价格接近短期支撑位时，成交量波动剧烈，这可能预示着市场情绪的不确定性增加或潜在的趋势变化。相较于参考因子，创新点在于用成交量的标准差代替了成交量的排名，更侧重于成交量的波动性而非相对大小，并结合了价格与近期支撑位的相对距离，通过比率形式衡量这种关系。
    因子应用场景：
    1. 市场情绪分析：可用于识别市场情绪不确定性增加的时期，尤其是在价格接近支撑位时。
    2. 趋势变化预警：因子值升高可能预示潜在的趋势变化。
    """
    # 1. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 20)
    # 2. 计算 ts_min_diff(close, 15)
    data_ts_min_diff_close = ts_min_diff(data['close'], 15)
    # 3. 计算 divide(ts_std_dev(vol, 20), ts_min_diff(close, 15))
    factor = divide(data_ts_std_dev_vol, data_ts_min_diff_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()