import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_rank, ts_delta, ts_std_dev, ts_skewness, ts_scale

import pandas as pd

def factor_5576(data, **kwargs):
    """
    因子名称: factor_0003_89285
    数学表达式: rank(ts_corr(ts_rank(high, 5), ts_rank(ts_delta(vol, 1), 5), 7)) + ts_rank(ts_std_dev(open, 15), 5) + ts_scale(ts_skewness(close,20))
    中文描述: 该因子在历史因子factor_0002的基础上，进一步结合了价格动量、量价关系、波动率和偏度信息，旨在更全面地评估股票的短期表现。

    1.  **更关注成交量变化**：
        *   将成交量变化率纳入量价关系计算中，使用ts_delta(vol, 1)计算每日成交量变化，并用ts_rank进行排序，从而捕捉成交量异动对价格的影响。

    2.  **更稳健的量价关系**：
        *   将ts_corr的时间窗口从10缩短到7，从而捕捉更短期的量价关系，降低长期噪音的影响，使因子对趋势的判断更加灵敏。

    应用场景：
       - 短期趋势跟踪：因子值较高可能表示价格趋势良好，可以作为趋势跟踪策略的信号。
       - 波动率交易：结合开盘价波动率信息，可以用于识别波动率较高的股票，进行波动率交易。
       - 风险评估：结合偏度信息，可以更好地评估股票的潜在风险。
       - 结合其他因子：该因子可以与其他因子（如价值因子、成长因子）结合使用，构建更稳健的选股模型。
    """
    # 1. 计算 ts_rank(high, 5)
    data_ts_rank_high = ts_rank(data['high'], 5)
    # 2. 计算 ts_delta(vol, 1)
    data_ts_delta_vol = ts_delta(data['vol'], 1)
    # 3. 计算 ts_rank(ts_delta(vol, 1), 5)
    data_ts_rank_ts_delta_vol = ts_rank(data_ts_delta_vol, 5)
    # 4. 计算 ts_corr(ts_rank(high, 5), ts_rank(ts_delta(vol, 1), 5), 7)
    data_ts_corr = ts_corr(data_ts_rank_high, data_ts_rank_ts_delta_vol, 7)
    # 5. 计算 rank(ts_corr(ts_rank(high, 5), ts_rank(ts_delta(vol, 1), 5), 7))
    data_rank_ts_corr = rank(data_ts_corr, 2)
    # 6. 计算 ts_std_dev(open, 15)
    data_ts_std_dev_open = ts_std_dev(data['open'], 15)
    # 7. 计算 ts_rank(ts_std_dev(open, 15), 5)
    data_ts_rank_ts_std_dev_open = ts_rank(data_ts_std_dev_open, 5)
    # 8. 计算 ts_skewness(close, 20)
    data_ts_skewness_close = ts_skewness(data['close'], 20)
    # 9. 计算 ts_scale(ts_skewness(close, 20))
    data_ts_scale_ts_skewness_close = ts_scale(data_ts_skewness_close)
    # 10. 计算 rank(ts_corr(ts_rank(high, 5), ts_rank(ts_delta(vol, 1), 5), 7)) + ts_rank(ts_std_dev(open, 15), 5) + ts_scale(ts_skewness(close,20))
    factor = data_rank_ts_corr + data_ts_rank_ts_std_dev_open + data_ts_scale_ts_skewness_close

    # 删除中间变量
    del data_ts_rank_high
    del data_ts_delta_vol
    del data_ts_rank_ts_delta_vol
    del data_ts_corr
    del data_rank_ts_corr
    del data_ts_std_dev_open
    del data_ts_rank_ts_std_dev_open
    del data_ts_skewness_close
    del data_ts_scale_ts_skewness_close

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()