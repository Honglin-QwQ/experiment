import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import multiply, ceiling, divide, ts_std_dev

def factor_6028(data, **kwargs):
    """
    因子名称: VolatilityAdjustedReturnsCeiling_51588
    数学表达式: multiply(returns, ceiling(divide(returns, ts_std_dev(returns, 10))))
    中文描述: 该因子是基于日收益率和其波动性的创新因子。首先计算日收益率除以过去10天的日收益率标准差，对收益率进行波动性调整。然后对调整后的收益率向上取整，最后将原始日收益率与向上取整后的波动性调整收益率相乘。这个因子旨在捕捉在波动性调整后，收益率向上突破的潜在机会。当收益率相对于其近期波动性表现出较强的上行趋势时，因子值会放大，可能用于识别短期内具有较强上涨动力的股票。
    因子应用场景：
    1. 波动性调整：用于识别在考虑波动性后，收益率表现出显著上行趋势的股票。
    2. 短期动量：捕捉短期内具有较强上涨动力的股票，尤其是在市场波动较大时。
    """
    # 1. 计算 ts_std_dev(returns, 10)
    data_ts_std_dev = ts_std_dev(data['returns'], 10)
    # 2. 计算 divide(returns, ts_std_dev(returns, 10))
    data_divide = divide(data['returns'], data_ts_std_dev)
    # 3. 计算 ceiling(divide(returns, ts_std_dev(returns, 10)))
    data_ceiling = ceiling(data_divide)
    # 4. 计算 multiply(returns, ceiling(divide(returns, ts_std_dev(returns, 10))))
    factor = multiply(data['returns'], data_ceiling)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()