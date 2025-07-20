import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_scale, ts_sum, subtract, divide, multiply, ts_corr, ts_delay, add

def factor_0031(data, **kwargs):
    """
    数学表达式: (ts_scale(((ts_sum(close, 7) / 7) - close)) + (20 * ts_scale(ts_corr(vwap, ts_delay(close, 5), 230)))) 
    中文描述: 该因子由两部分组成，第一部分计算过去7天收盘价均值与当天收盘价的差值，并进行标准化；第二部分计算成交量加权平均价与5天前收盘价在过去230天的相关性，乘以20后再标准化，最后将两部分相加，该因子试图结合价格的短期均值偏离和中长期的量价相关性来预测股票的未来表现，可能捕捉价格短期反转和长期趋势共振的信号，可用于构建量化选股策略，例如，选择因子值较高的股票构建多头组合，或用于高频交易中，结合其他因子判断短期价格波动方向。
    因子应用场景：
    1. 量化选股：选择因子值较高的股票构建多头组合，预期这些股票可能具有较好的未来表现。
    2. 高频交易：结合其他因子判断短期价格波动方向，辅助决策。
    3. 风险管理：监控因子值的变化，及时调整仓位，控制风险。
    """
    # 1. 计算 ts_sum(close, 7)
    ts_sum_close = ts_sum(data['close'], 7)
    # 2. 计算 (ts_sum(close, 7) / 7)
    avg_close = divide(ts_sum_close, 7)
    # 3. 计算 ((ts_sum(close, 7) / 7) - close)
    diff = subtract(avg_close, data['close'])
    # 4. 计算 ts_scale(((ts_sum(close, 7) / 7) - close))
    part1 = ts_scale(diff)
    # 5. 计算 ts_delay(close, 5)
    ts_delay_close = ts_delay(data['close'], 5)
    # 6. 计算 ts_corr(vwap, ts_delay(close, 5), 230)
    ts_corr_vwap_close = ts_corr(data['vwap'], ts_delay_close, 230)
    # 7. 计算 20 * ts_scale(ts_corr(vwap, ts_delay(close, 5), 230))
    part2 = multiply(20, ts_scale(ts_corr_vwap_close))
    # 8. 计算 (ts_scale(((ts_sum(close, 7) / 7) - close)) + (20 * ts_scale(ts_corr(vwap, ts_delay(close, 5), 230))))
    factor = add(part1, part2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()