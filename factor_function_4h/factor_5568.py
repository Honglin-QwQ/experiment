import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_rank, ts_std_dev, ts_scale, ts_skewness

def factor_5568(data, **kwargs):
    """
    数学表达式: rank(ts_corr(ts_rank(high, 5), vwap, 10)) + ts_rank(ts_std_dev(open, 20), 5) + ts_scale(ts_skewness(close,15))
    中文描述: 该因子在历史因子factor_0001的基础上，进一步结合了价格动量、量价关系、波动率和偏度信息，旨在更全面地评估股票的短期表现。

    1.  **更稳健的量价关系**：
        *   将ts_corr的时间窗口从5增加到10，从而捕捉更长期的量价关系，降低短期噪音的影响，使因子对趋势的判断更加稳健。

    2.  **更全面的波动率信息**：
        *   将ts_std_dev的时间窗口从15增加到20，从而捕捉更长期的价格波动，使因子对风险的评估更加全面。

    3.  **偏度信息的引入**：
        *   引入ts_skewness(close,15)来衡量收盘价分布的偏度，从而捕捉价格分布的非对称性，更好地识别潜在的上涨或下跌风险。ts_scale用于标准化偏度值，使其与其他因子具有可比性。

    应用场景：
       - 短期趋势跟踪：因子值较高可能表示价格趋势良好，可以作为趋势跟踪策略的信号。
       - 波动率交易：结合开盘价波动率信息，可以用于识别波动率较高的股票，进行波动率交易。
       - 风险评估：结合偏度信息，可以更好地评估股票的潜在风险。
       - 结合其他因子：该因子可以与其他因子（如价值因子、成长因子）结合使用，构建更稳健的选股模型。
    """
    # 1. 计算 ts_rank(high, 5)
    data_ts_rank_high = ts_rank(data['high'], 5)
    # 2. 计算 ts_corr(ts_rank(high, 5), vwap, 10)
    data_ts_corr = ts_corr(data_ts_rank_high, data['vwap'], 10)
    # 3. 计算 rank(ts_corr(ts_rank(high, 5), vwap, 10))
    factor1 = rank(data_ts_corr, 2)
    # 4. 计算 ts_std_dev(open, 20)
    data_ts_std_dev_open = ts_std_dev(data['open'], 20)
    # 5. 计算 ts_rank(ts_std_dev(open, 20), 5)
    factor2 = ts_rank(data_ts_std_dev_open, 5)
    # 6. 计算 ts_skewness(close, 15)
    data_ts_skewness_close = ts_skewness(data['close'], 15)
    # 7. 计算 ts_scale(ts_skewness(close,15))
    factor3 = ts_scale(data_ts_skewness_close)
    # 8. 计算 rank(ts_corr(ts_rank(high, 5), vwap, 10)) + ts_rank(ts_std_dev(open, 20), 5) + ts_scale(ts_skewness(close,15))
    factor = factor1 + factor2 + factor3

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()