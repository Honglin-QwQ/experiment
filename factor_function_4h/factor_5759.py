import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_zscore, ts_delta, divide, multiply

def factor_5759(data, **kwargs):
    """
    因子名称: OpenZscoreVolatilityRatio_40296
    数学表达式: divide(ts_std_dev(open * ts_zscore(open, 111), 66), ts_std_dev(ts_delta(open, 3), 66))
    中文描述: 该因子计算开盘价乘以其长期Z分数的时间序列标准差，并将其除以开盘价短期变化的时间序列标准差。分子衡量的是开盘价与其长期相对位置结合后的波动性，分母衡量的是开盘价短期变化的波动性。这个比值可能反映了开盘价的波动是主要由其相对于历史均值的偏离驱动，还是由短期的价格跳动驱动。创新点在于结合了开盘价的绝对值、长期相对位置以及短期变化，通过比值形式捕捉不同来源波动性的相对强度。
    因子应用场景：
    1. 波动性分析：用于分析开盘价波动性的来源，是受长期相对位置影响还是短期价格跳动影响。
    2. 趋势判断：结合因子值变化，辅助判断市场趋势的稳定性和持续性。
    3. 风险评估：评估由开盘价波动带来的潜在风险。
    """
    # 1. 计算 ts_zscore(open, 111)
    data_ts_zscore_open = ts_zscore(data['open'], d=111)
    # 2. 计算 open * ts_zscore(open, 111)
    data_open_mult_ts_zscore_open = multiply(data['open'], data_ts_zscore_open)
    # 3. 计算 ts_std_dev(open * ts_zscore(open, 111), 66)
    data_ts_std_dev_numerator = ts_std_dev(data_open_mult_ts_zscore_open, d=66)
    # 4. 计算 ts_delta(open, 3)
    data_ts_delta_open = ts_delta(data['open'], d=3)
    # 5. 计算 ts_std_dev(ts_delta(open, 3), 66)
    data_ts_std_dev_denominator = ts_std_dev(data_ts_delta_open, d=66)
    # 6. 计算 divide(ts_std_dev(open * ts_zscore(open, 111), 66), ts_std_dev(ts_delta(open, 3), 66))
    factor = divide(data_ts_std_dev_numerator, data_ts_std_dev_denominator)

    # 删除中间变量
    del data_ts_zscore_open
    del data_open_mult_ts_zscore_open
    del data_ts_std_dev_numerator
    del data_ts_delta_open
    del data_ts_std_dev_denominator

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()