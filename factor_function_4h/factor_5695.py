import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, kth_element, ts_zscore, abs, divide

def factor_5695(data, **kwargs):
    """
    因子名称: VWAP_ZScore_Volatility_Ratio_24029
    数学表达式: divide(ts_std_dev(kth_element(vwap, 6, k=1), 6), abs(ts_zscore(kth_element(vwap, 6, k=1), 6)))
    中文描述: 该因子旨在衡量VWAP的标准化波动性相对于其标准化偏差的比例。首先，使用kth_element(vwap, 6, k=1)获取最近6天内的第一个有效VWAP值，以平滑短期波动。
    然后，计算这个平滑VWAP值在过去6天内的标准差 (ts_std_dev) 和Z分数 (ts_zscore)。最后，将标准差除以Z分数的绝对值。
    这个比例可以反映出在考虑了VWAP相对于其均值的偏移程度后，其自身的波动性水平。较高的因子值可能表明VWAP在相对于其均值有显著偏移的同时，仍然表现出较高的波动性，
    这可能预示着价格的不确定性或潜在的反转机会。相较于参考因子，创新点在于将VWAP的波动性和标准化偏差结合起来，形成一个比例，从而更全面地评估VWAP的动态特征。
    因子应用场景：
    1. 波动性分析：用于识别VWAP波动性相对于其均值偏移程度较高的股票。
    2. 反转信号：较高的因子值可能预示着潜在的价格反转机会。
    3. 趋势确认：结合其他技术指标，辅助确认当前趋势的强度和持续性。
    """
    # 1. 计算 kth_element(vwap, 6, k=1)
    data_kth_element = kth_element(data['vwap'], 6, k=1)
    # 2. 计算 ts_std_dev(kth_element(vwap, 6, k=1), 6)
    data_ts_std_dev = ts_std_dev(data_kth_element, 6)
    # 3. 计算 ts_zscore(kth_element(vwap, 6, k=1), 6)
    data_ts_zscore = ts_zscore(data_kth_element, 6)
    # 4. 计算 abs(ts_zscore(kth_element(vwap, 6, k=1), 6))
    data_abs_ts_zscore = abs(data_ts_zscore)
    # 5. 计算 divide(ts_std_dev(kth_element(vwap, 6, k=1), 6), abs(ts_zscore(kth_element(vwap, 6, k=1), 6)))
    factor = divide(data_ts_std_dev, data_abs_ts_zscore)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()