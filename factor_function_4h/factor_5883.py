import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, divide, ts_min_diff, ts_sum

def factor_5883(data, **kwargs):
    """
    因子名称: VolOpenDiffZScore_55621
    数学表达式: ts_zscore(divide(ts_min_diff(open, 48), ts_sum(vol, 97)), 28)
    中文描述: 该因子结合了开盘价的最小差分和成交量的标准化信息。它首先计算过去48天开盘价与最低开盘价的差值，然后将这个差值除以过去97天的总成交量，得到一个单位成交量下的开盘价波动指标。最后，计算这个指标在过去28天内的Z分数。这个因子旨在捕捉在不同成交量水平下，开盘价相对于近期低点的波动程度的异常情况。高Z分数可能表明在相对较低的成交量下，开盘价出现了显著上涨，这可能预示着潜在的买入机会或市场情绪的积极变化。相较于参考因子，该因子通过引入成交量作为权重对开盘价波动进行标准化，并进一步计算Z分数来衡量其异常性，具有更强的创新性和信息含量。
    因子应用场景：
    1. 异常波动检测：用于检测在成交量较低的情况下，开盘价的异常波动。
    2. 买入机会识别：高Z分数可能指示潜在的买入机会。
    3. 市场情绪分析：反映市场对特定股票或行业的乐观程度。
    """
    # 1. 计算 ts_min_diff(open, 48)
    data_ts_min_diff_open = ts_min_diff(data['open'], 48)
    # 2. 计算 ts_sum(vol, 97)
    data_ts_sum_vol = ts_sum(data['vol'], 97)
    # 3. 计算 divide(ts_min_diff(open, 48), ts_sum(vol, 97))
    data_divide = divide(data_ts_min_diff_open, data_ts_sum_vol)
    # 4. 计算 ts_zscore(divide(ts_min_diff(open, 48), ts_sum(vol, 97)), 28)
    factor = ts_zscore(data_divide, 28)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()