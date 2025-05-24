import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_covariance

def factor_5742(data, **kwargs):
    """
    因子名称: Price_Volume_Anomaly_Score_72288
    数学表达式: ts_zscore(ts_covariance(high, vol, 5), 20) - ts_zscore(ts_covariance(low, amount, 5), 20)
    中文描述: 该因子计算了基于高价与成交量协方差的短期Z分数与基于低价与交易额协方差的短期Z分数之差。具体而言，首先计算过去5天内最高价与成交量的协方差，以及最低价与交易额的协方差。然后，分别计算这两个协方差序列在过去20天内的Z分数。最后，用高价/成交量协方差的Z分数减去低价/交易额协方差的Z分数。该因子旨在捕捉价格波动与成交活动之间的短期异常关系。正值可能表示高价伴随高成交量，而低价伴随低交易额，暗示市场存在追高情绪或潜在的顶部信号。负值则可能表示低价伴随高交易额，而高价伴随低成交量，暗示市场存在抄底情绪或潜在的底部信号。创新点在于结合了不同价格水平（高价和低价）与不同成交指标（成交量和交易额）的协方差，并通过Z分数进行标准化和比较，以识别短期内的价格-成交异常模式。
    因子应用场景：
    1. 异常检测：识别价格与成交量/交易额之间短期内不寻常的关系，辅助判断市场情绪和潜在转折点。
    2. 趋势确认：结合因子值和价格趋势，验证当前趋势的可靠性。例如，若价格上涨且因子值为正，可能表明上涨趋势得到成交量的支持。
    3. 交易信号：当因子值达到极端水平时，可能预示着超买或超卖情况，从而产生交易信号。
    """
    # 1. 计算 ts_covariance(high, vol, 5)
    data_ts_covariance_high_vol = ts_covariance(data['high'], data['vol'], 5)
    # 2. 计算 ts_zscore(ts_covariance(high, vol, 5), 20)
    data_ts_zscore_high_vol = ts_zscore(data_ts_covariance_high_vol, 20)
    # 3. 计算 ts_covariance(low, amount, 5)
    data_ts_covariance_low_amount = ts_covariance(data['low'], data['amount'], 5)
    # 4. 计算 ts_zscore(ts_covariance(low, amount, 5), 20)
    data_ts_zscore_low_amount = ts_zscore(data_ts_covariance_low_amount, 20)
    # 5. 计算 ts_zscore(ts_covariance(high, vol, 5), 20) - ts_zscore(ts_covariance(low, amount, 5), 20)
    factor = data_ts_zscore_high_vol - data_ts_zscore_low_amount

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()