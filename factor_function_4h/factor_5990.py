import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log, divide, add, densify, ts_std_dev

def factor_5990(data, **kwargs):
    """
    因子名称: LogClose_VolatilityAdjustedReturnsRatio_82797
    数学表达式: divide(log(close), add(densify(returns), ts_std_dev(returns, 10)))
    中文描述: 该因子在原有LogClose_ReturnsDensityRatio因子的基础上进行了改进。分子仍然是对收盘价取自然对数，用于平滑价格并捕捉长期趋势。分母则在收益率密集化的基础上，加入了过去10天收益率的标准差。通过将对数收盘价除以收益率的密集化和波动率之和，该因子旨在捕捉在价格趋势相对平缓（log(close)变化不大）但收益率波动较大且集中的情况下，可能存在的交易机会。相较于原因子，引入收益率标准差增加了对风险的考量，可能有助于识别风险调整后的潜在机会。这符合改进建议中引入波动率信息的方向，并利用了可用的ts_std_dev操作符。
    因子应用场景：
    1. 波动率调整：在收益率密集的情况下，通过引入波动率因素，筛选出风险调整后的潜在交易机会。
    2. 趋势平缓期：当价格趋势不明显时，该因子可以帮助识别收益率波动较大且集中的股票。
    """
    # 1. 计算 log(close)
    data_log_close = log(data['close'])
    # 2. 计算 densify(returns)
    data_densify_returns = densify(data['returns'])
    # 3. 计算 ts_std_dev(returns, 10)
    data_ts_std_dev_returns = ts_std_dev(data['returns'], 10)
    # 4. 计算 add(densify(returns), ts_std_dev(returns, 10))
    data_add_densify_ts_std_dev = add(data_densify_returns, data_ts_std_dev_returns)
    # 5. 计算 divide(log(close), add(densify(returns), ts_std_dev(returns, 10)))
    factor = divide(data_log_close, data_add_densify_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()