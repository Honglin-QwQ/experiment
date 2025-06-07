import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, subtract, multiply,add

def factor_0034(data, **kwargs):
    """
    数学表达式: ((ts_rank(volume, 32) * (1 - ts_rank(((close + high) - low), 16))) * (1 - ts_rank(returns, 32))) 
    中文描述: 描述：该因子综合考虑了成交量、价格波动和收益率三个因素，首先计算过去32天成交量排名的百分比，然后计算过去16天内每日（最高价+收盘价-最低价）的排名百分比，用1减去该百分比，衡量价格波动的大小，最后计算过去32天收益率的排名百分比，同样用1减去该百分比，衡量收益率的稳定性，将三个结果相乘，得到最终的因子值，该因子值越高，表明成交量越高、价格波动越小、收益率越稳定。
    应用场景：
    1. 选股策略：选择因子值较高的股票，预期这些股票具有较好的流动性、较低的风险和稳定的收益。
    2. 风险控制：监控因子值较低的股票，警惕这些股票可能存在的流动性风险、价格波动风险或收益不稳定风险。
    3. 量化择时：结合大盘走势，当因子值整体上升时，可能预示市场风险偏好下降，可适当降低仓位。
    """
    # 1. 计算 ts_rank(volume, 32)
    data_ts_rank_volume = ts_rank(data['vol'], 32)
    # 2. 计算 (close + high) - low
    data_price_diff = subtract(add(data['close'], data['high']), data['low'], filter = False)
    # 3. 计算 ts_rank(((close + high) - low), 16)
    data_ts_rank_price_diff = ts_rank(data_price_diff, 16)
    # 4. 计算 1 - ts_rank(((close + high) - low), 16)
    data_one_minus_ts_rank_price_diff = subtract(1, data_ts_rank_price_diff, filter = False)
    # 5. 计算 ts_rank(returns, 32)
    data_ts_rank_returns = ts_rank(data['returns'], 32)
    # 6. 计算 1 - ts_rank(returns, 32)
    data_one_minus_ts_rank_returns = subtract(1, data_ts_rank_returns, filter = False)
    # 7. 计算 (ts_rank(volume, 32) * (1 - ts_rank(((close + high) - low), 16))) * (1 - ts_rank(returns, 32))
    factor = multiply(data_ts_rank_volume, data_one_minus_ts_rank_price_diff, data_one_minus_ts_rank_returns, filter = False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()