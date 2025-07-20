import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delay, subtract, add

def factor_0036(data, **kwargs):
    """
    数学表达式: (rank(ts_corr(ts_delay((open - close), 1), close, 200)) + rank((open - close)))
    中文描述: 该因子首先计算过去200天每天的开盘价减收盘价与收盘价的相关性，然后对相关性进行排序；同时计算当天的开盘价减收盘价，并进行排序；最后将两个排序结果相加。这个因子试图捕捉股价趋势反转的信号，一方面衡量了近期日内价格变化与收盘价的关联程度，另一方面直接反映了当日价格变化的方向，将两者结合可以辅助判断潜在的交易机会。
    因子应用场景：
    1. 短线择时：因子值较高可能预示着潜在的买入机会，反之则可能是卖出信号。
    2. 量化选股：结合其他基本面或技术面因子，筛选出因子值较高的股票，构建股票组合。
    3. 风险控制：监控因子值的异常波动，及时调整仓位，降低投资风险。
    """
    # 1. 计算 (open - close)
    open_minus_close = subtract(data['open'], data['close'])
    # 2. 计算 ts_delay((open - close), 1)
    ts_delay_open_minus_close = ts_delay(open_minus_close, 1)
    # 3. 计算 ts_corr(ts_delay((open - close), 1), close, 200)
    ts_corr_result = ts_corr(ts_delay_open_minus_close, data['close'], 200)
    # 4. 计算 rank(ts_corr(ts_delay((open - close), 1), close, 200))
    rank_ts_corr = rank(ts_corr_result, 2)
    # 5. 计算 rank((open - close))
    rank_open_minus_close = rank(open_minus_close, 2)
    # 6. 计算 (rank(ts_corr(ts_delay((open - close), 1), close, 200)) + rank((open - close)))
    factor = add(rank_ts_corr, rank_open_minus_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()