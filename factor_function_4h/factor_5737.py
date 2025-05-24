import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, rank, divide, ts_skewness, ts_delay, ts_kurtosis

def factor_5737(data, **kwargs):
    """
    数学表达式: subtract(rank(divide(subtract(ts_skewness(vol, 10), ts_delay(ts_skewness(vol, 10), 5)), ts_delay(ts_skewness(vol, 10), 5))), rank(divide(subtract(ts_kurtosis(vol, 10), ts_delay(ts_kurtosis(vol, 10), 5)), ts_delay(ts_kurtosis(vol, 10), 5))))
    中文描述: 该因子基于对历史评估结果的分析和改进建议，旨在捕捉成交量分布偏度和峰度的短期变化率。它首先计算过去10天成交量序列的偏度和峰度，然后计算这两者相对于5天前值的变化率。最后，计算偏度变化率的截面排名与峰度变化率的截面排名之差。通过关注变化率而非绝对值或其排名，该因子试图捕捉成交量分布形态的动态演变。当偏度变化率排名显著高于峰度变化率排名时，可能预示着成交量分布向高值倾斜的趋势正在增强，而极端值出现的可能性增加的趋势相对减弱；反之亦然。这种变化率的相对排名差异可能更好地反映市场情绪或交易行为模式的短期转变，从而提供更具时效性的交易信号。相较于原因子，创新点在于使用了变化率的概念，并缩短了计算偏度和峰度的窗口期（从20天缩短到10天），以期捕捉更短期的市场动态，并根据改进建议使用了divide和subtract等操作符来计算变化率。
    因子应用场景：
    1. 市场情绪分析：该因子可用于识别市场情绪的短期转变，尤其是在成交量分布的偏度和峰度发生显著变化时。
    2. 交易信号生成：通过监测偏度变化率和峰度变化率的相对排名差异，可以生成更具时效性的交易信号。
    3. 风险管理：该因子有助于评估市场风险，尤其是在成交量分布形态发生剧烈变化时。
    """
    # 1. 计算 ts_skewness(vol, 10)
    data_ts_skewness_vol = ts_skewness(data['vol'], 10)
    # 2. 计算 ts_delay(ts_skewness(vol, 10), 5)
    data_ts_delay_ts_skewness_vol = ts_delay(data_ts_skewness_vol, 5)
    # 3. 计算 subtract(ts_skewness(vol, 10), ts_delay(ts_skewness(vol, 10), 5))
    data_subtract_skewness = subtract(data_ts_skewness_vol, data_ts_delay_ts_skewness_vol)
    # 4. 计算 divide(subtract(ts_skewness(vol, 10), ts_delay(ts_skewness(vol, 10), 5)), ts_delay(ts_skewness(vol, 10), 5))
    data_divide_skewness = divide(data_subtract_skewness, data_ts_delay_ts_skewness_vol)
    # 5. 计算 rank(divide(subtract(ts_skewness(vol, 10), ts_delay(ts_skewness(vol, 10), 5)), ts_delay(ts_skewness(vol, 10), 5)))
    data_rank_skewness = rank(data_divide_skewness, 2)

    # 6. 计算 ts_kurtosis(vol, 10)
    data_ts_kurtosis_vol = ts_kurtosis(data['vol'], 10)
    # 7. 计算 ts_delay(ts_kurtosis(vol, 10), 5)
    data_ts_delay_ts_kurtosis_vol = ts_delay(data_ts_kurtosis_vol, 5)
    # 8. 计算 subtract(ts_kurtosis(vol, 10), ts_delay(ts_kurtosis(vol, 10), 5))
    data_subtract_kurtosis = subtract(data_ts_kurtosis_vol, data_ts_delay_ts_kurtosis_vol)
    # 9. 计算 divide(subtract(ts_kurtosis(vol, 10), ts_delay(ts_kurtosis(vol, 10), 5)), ts_delay(ts_kurtosis(vol, 10), 5))
    data_divide_kurtosis = divide(data_subtract_kurtosis, data_ts_delay_ts_kurtosis_vol)
    # 10. 计算 rank(divide(subtract(ts_kurtosis(vol, 10), ts_delay(ts_kurtosis(vol, 10), 5)), ts_delay(ts_kurtosis(vol, 10), 5)))
    data_rank_kurtosis = rank(data_divide_kurtosis, 2)

    # 11. 计算 subtract(rank(divide(subtract(ts_skewness(vol, 10), ts_delay(ts_skewness(vol, 10), 5)), ts_delay(ts_skewness(vol, 10), 5))), rank(divide(subtract(ts_kurtosis(vol, 10), ts_delay(ts_kurtosis(vol, 10), 5)), ts_delay(ts_kurtosis(vol, 10), 5))))
    factor = subtract(data_rank_skewness, data_rank_kurtosis)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()