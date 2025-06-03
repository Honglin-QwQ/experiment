import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, subtract, add

def factor_0100(data, **kwargs):
    """
    数学表达式: ((close - open) / ((high - low) + .001))
    中文描述: 这个因子计算的是每天股价的涨跌幅相对于当日价格波动范围的比例，其中价格波动范围通过最高价减去最低价得到，为了避免除以零的情况，加上了一个很小的数值0.001。它衡量了当日价格变化相对于价格波动区间的程度，正值表示收盘价高于开盘价，负值表示收盘价低于开盘价，绝对值越大表示当日价格变化相对于波动范围越大。
    因子应用场景:
    1. 短线择时：可以用来识别日内强势或弱势的股票，例如，高正值的股票可能意味着买盘强劲，适合短线买入。
    2. 波动率指标：结合历史数据，可以作为衡量股价波动剧烈程度的指标，用于构建波动率相关的交易策略。
    3. 异动检测：可以用来识别当日股价走势异常的股票，例如，在平静的市场中，该因子出现极端值可能预示着潜在的利好或利空消息。
    """
    # 1. 计算 (close - open)
    close_minus_open = subtract(data['close'], data['open'])
    # 2. 计算 (high - low)
    high_minus_low = subtract(data['high'], data['low'])
    # 3. 计算 ((high - low) + .001)
    high_minus_low_plus_001 = add(high_minus_low, 0.001)
    # 4. 计算 ((close - open) / ((high - low) + .001))
    factor = divide(close_minus_open, high_minus_low_plus_001)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()