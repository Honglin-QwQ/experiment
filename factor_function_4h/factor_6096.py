import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_std_dev, ts_delta, divide

def factor_6096(data, **kwargs):
    """
    因子名称: OpenPriceRankVolatilityRatio_22467
    数学表达式: divide(ts_rank(open, 116), ts_std_dev(ts_delta(open, 3), 22))
    中文描述: 该因子结合了开盘价在长时间窗口内的排名和开盘价短期变化的波动性。首先计算当前开盘价在过去116天开盘价中的排名，反映开盘价的相对强势。然后计算过去22天内三天开盘价变化的 标准差，衡量开盘价短期波动的剧烈程度。最后，将开盘价排名除以开盘价短期变化的 标准差。该因子旨在识别那些在长期内表现相对强势（排名高），但短期波动性较低的股票，可能指示价格趋势的稳定性。创新点在于结合了长期排名和短期波动性，并使用除法构建了新的关系。
    因子应用场景：
    1. 趋势识别：识别长期强势但短期波动性低的股票，可能预示稳定上涨趋势。
    2. 稳定性筛选：筛选价格波动性相对较低的股票，适合风险厌恶型投资者。
    """
    # 1. 计算 ts_rank(open, 116)
    data_ts_rank_open = ts_rank(data['open'], 116)
    # 2. 计算 ts_delta(open, 3)
    data_ts_delta_open = ts_delta(data['open'], 3)
    # 3. 计算 ts_std_dev(ts_delta(open, 3), 22)
    data_ts_std_dev = ts_std_dev(data_ts_delta_open, 22)
    # 4. 计算 divide(ts_rank(open, 116), ts_std_dev(ts_delta(open, 3), 22))
    factor = divide(data_ts_rank_open, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()