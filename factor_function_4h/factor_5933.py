import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, ts_rank, adv, ts_std_dev, ts_delta

def factor_5933(data, **kwargs):
    """
    数学表达式: subtract(ts_rank(adv(vol, 10), 13), ts_rank(ts_std_dev(ts_delta(close, 1), 22), 13))
    中文描述: 该因子旨在衡量在不同时间窗口下，成交量排名与价格波动率排名之间的差异。它首先计算过去10天平均成交量在过去13天内的排名，反映近期成交量的相对活跃程度。
    然后，计算过去22天内1天收盘价变化的标准差（衡量短期波动率）在过去13天内的排名。最后，将成交量排名减去波动率排名。
    当成交量排名较高而波动率排名较低时，因子值较高，可能指示在相对活跃的交易中，价格波动受到抑制，这可能与资金的温和流入或市场情绪的稳定有关。
    创新点在于结合了不同时间窗口的成交量和波动率排名，并通过相减的方式突出它们之间的相对强弱关系，同时使用了收盘价的短期变化来衡量波动率，
    而非参考因子的开盘价长期变化，并根据改进建议调整了时间窗口参数，以提高因子的预测能力。
    因子应用场景：
    1. 市场情绪分析：用于识别市场中成交量活跃但波动率较低的股票，可能反映市场情绪稳定。
    2. 交易信号：因子值较高可能指示买入机会，表明资金流入但价格波动不大。
    """
    # 1. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], d = 10)
    # 2. 计算 ts_rank(adv(vol, 10), 13)
    data_ts_rank_adv_vol = ts_rank(data_adv_vol, d = 13)
    # 3. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], d = 1)
    # 4. 计算 ts_std_dev(ts_delta(close, 1), 22)
    data_ts_std_dev_ts_delta_close = ts_std_dev(data_ts_delta_close, d = 22)
    # 5. 计算 ts_rank(ts_std_dev(ts_delta(close, 1), 22), 13)
    data_ts_rank_ts_std_dev_ts_delta_close = ts_rank(data_ts_std_dev_ts_delta_close, d = 13)
    # 6. 计算 subtract(ts_rank(adv(vol, 10), 13), ts_rank(ts_std_dev(ts_delta(close, 1), 22), 13))
    factor = subtract(data_ts_rank_adv_vol, data_ts_rank_ts_std_dev_ts_delta_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()