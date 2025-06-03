import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_min, ts_delta, ts_max, multiply

def factor_0009(data, **kwargs):
    """
    数学表达式: rank(((0 < ts_min(ts_delta(close, 1), 4)) ? ts_delta(close, 1) : ((ts_max(ts_delta(close, 1), 4) < 0) ? ts_delta(close, 1) : (-1 * ts_delta(close, 1)))))
    中文描述: 如果过去4天每天的收盘价涨跌都是上涨，则取当天的收盘价涨跌；如果过去4天每天的收盘价涨跌都是下跌，则取当天的收盘价涨跌；否则取当天收盘价涨跌的相反数，最后对结果进行排序，得到一个相对排名。该因子可以用于识别趋势极端反转的股票，例如：1. 寻找短期内持续上涨后可能下跌的股票；2. 寻找短期内持续下跌后可能反弹的股票；3. 结合其他技术指标，构建更复杂的交易策略。
    因子应用场景：
    1. 识别趋势反转：该因子可以帮助识别短期内趋势可能发生反转的股票。
    2. 辅助交易决策：结合其他技术指标，可以构建更复杂的交易策略，例如在趋势反转信号出现时进行买入或卖出操作。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    
    # 2. 计算 ts_min(ts_delta(close, 1), 4)
    data_ts_min = ts_min(data_ts_delta_close, 4)
    
    # 3. 计算 ts_max(ts_delta(close, 1), 4)
    data_ts_max = ts_max(data_ts_delta_close, 4)
    
    # 4. 计算 -1 * ts_delta(close, 1)
    data_neg_ts_delta_close = multiply(-1, data_ts_delta_close)
    
    # 5. 计算条件表达式
    condition1 = 0 < data_ts_min
    condition2 = data_ts_max < 0
    
    # 6. 根据条件选择不同的值
    factor = data_ts_delta_close.where(condition1, data_ts_delta_close.where(condition2, data_neg_ts_delta_close))
    
    # 7. 计算 rank(result)
    factor = rank(factor, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()