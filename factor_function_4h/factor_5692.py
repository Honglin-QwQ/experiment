import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log, divide, ts_sum, ts_rank, ts_delta, ts_corr, sigmoid, ts_skewness, multiply

def factor_5692(data, **kwargs):
    """
    因子名称: factor_0003_30901
    数学表达式: ts_rank(divide(ts_sum(log(tbase), 5), ts_sum(log(tquote), 5)), 10) * ts_delta(ts_corr(close, vol, 5), 2) * sigmoid(ts_skewness(ts_delta(close,1),5))
    中文描述: 该因子在历史因子factor_0002的基础上进行了改进，保留了ts_rank(divide(ts_sum(log(tbase), 5), ts_sum(log(tquote), 5)), 10) * ts_delta(ts_corr(close, vol, 5), 2)部分，该部分衡量了短期内买盘力量相对于卖盘力量的强度，并通过排名来识别买盘力量相对较强的时期，同时考虑了价量关系的短期变化。同时，创新性地引入了sigmoid(ts_skewness(ts_delta(close,1),5))项，该项计算过去5日收盘价差值的偏度，并使用sigmoid函数将其映射到0到1之间，从而反映了价格变化分布的偏斜程度。该因子旨在衡量短期内买盘力量相对于卖盘力量的强度，并通过排名来识别买盘力量相对较强的时期，同时考虑了价量关系的短期变化，以及价格变化分布的偏斜程度，可能更有效地捕捉市场情绪的转变。
    因子应用场景：
    1. 衡量买卖盘力量：用于衡量短期内买盘力量相对于卖盘力量的强度。
    2. 识别市场情绪转变：结合价格变化分布的偏斜程度，捕捉市场情绪的转变。
    3. 辅助交易决策：结合其他技术指标和基本面数据，辅助交易决策。
    """
    # 1. 计算 log(tbase)
    data['log_tbase'] = log(data['tbase'])
    # 2. 计算 ts_sum(log(tbase), 5)
    data['ts_sum_log_tbase'] = ts_sum(data['log_tbase'], 5)
    # 3. 计算 log(tquote)
    data['log_tquote'] = log(data['tquote'])
    # 4. 计算 ts_sum(log(tquote), 5)
    data['ts_sum_log_tquote'] = ts_sum(data['log_tquote'], 5)
    # 5. 计算 divide(ts_sum(log(tbase), 5), ts_sum(log(tquote), 5))
    data['divide_sum_log'] = divide(data['ts_sum_log_tbase'], data['ts_sum_log_tquote'])
    # 6. 计算 ts_rank(divide(ts_sum(log(tbase), 5), ts_sum(log(tquote), 5)), 10)
    data['ts_rank_divide'] = ts_rank(data['divide_sum_log'], 10)
    # 7. 计算 ts_corr(close, vol, 5)
    data['ts_corr_close_vol'] = ts_corr(data['close'], data['vol'], 5)
    # 8. 计算 ts_delta(ts_corr(close, vol, 5), 2)
    data['ts_delta_corr'] = ts_delta(data['ts_corr_close_vol'], 2)
    # 9. 计算 ts_delta(close, 1)
    data['ts_delta_close'] = ts_delta(data['close'], 1)
    # 10. 计算 ts_skewness(ts_delta(close,1),5)
    data['ts_skewness_delta'] = ts_skewness(data['ts_delta_close'], 5)
    # 11. 计算 sigmoid(ts_skewness(ts_delta(close,1),5))
    data['sigmoid_skewness'] = sigmoid(data['ts_skewness_delta'])
    # 12. 计算 ts_rank(divide(ts_sum(log(tbase), 5), ts_sum(log(tquote), 5)), 10) * ts_delta(ts_corr(close, vol, 5), 2) * sigmoid(ts_skewness(ts_delta(close,1),5))
    factor = multiply(data['ts_rank_divide'], data['ts_delta_corr'], data['sigmoid_skewness'])

    data.drop(columns=['log_tbase', 'ts_sum_log_tbase', 'log_tquote', 'ts_sum_log_tquote', 'divide_sum_log',
                       'ts_rank_divide', 'ts_corr_close_vol', 'ts_delta_corr', 'ts_delta_close',
                       'ts_skewness_delta', 'sigmoid_skewness'], inplace=True)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()