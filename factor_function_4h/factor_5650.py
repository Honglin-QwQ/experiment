import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import multiply, ts_returns, ts_rank, divide, ts_std_dev, ts_corr

def factor_5650(data, **kwargs):
    """
    因子名称: VolatilityAdjustedReturnMomentum_11959
    数学表达式: multiply(ts_returns(close, 20), ts_rank(divide(ts_std_dev(returns, 10), ts_std_dev(returns, 30)), 10), ts_corr(close, vol, 5))
    中文描述: 该因子旨在结合中长期收益率动量、波动率变化和量价关系来识别潜在的投资机会。首先，计算过去20天的收益率，捕捉中长期的价格动量。然后，计算短期（10天）和长期（30天）波动率的比率，并进行排名，衡量波动率的变化趋势。最后，计算过去5天收盘价与成交量的相关性，反映量价关系。将收益率、波动率变化排名和量价关系相关性相乘，旨在捕捉在中长期上涨趋势中，短期波动率下降且量价关系健康的股票。相较于历史因子，本因子更侧重于波动率结构的变化，并结合了量价关系，逻辑上更为完善。
    因子应用场景：
    1. 趋势识别：识别在中长期上涨趋势中，短期波动率下降且量价关系健康的股票。
    2. 波动率分析：捕捉波动率变化趋势，辅助判断市场风险。
    3. 量价关系：结合量价关系，验证价格趋势的可靠性。
    """
    # 1. 计算 ts_returns(close, 20)
    data_ts_returns = ts_returns(data['close'], 20)
    # 2. 计算 ts_std_dev(returns, 10)
    data_ts_std_dev_10 = ts_std_dev(data['returns'], 10)
    # 3. 计算 ts_std_dev(returns, 30)
    data_ts_std_dev_30 = ts_std_dev(data['returns'], 30)
    # 4. 计算 divide(ts_std_dev(returns, 10), ts_std_dev(returns, 30))
    data_divide = divide(data_ts_std_dev_10, data_ts_std_dev_30)
    # 5. 计算 ts_rank(divide(ts_std_dev(returns, 10), ts_std_dev(returns, 30)), 10)
    data_ts_rank = ts_rank(data_divide, 10)
    # 6. 计算 ts_corr(close, vol, 5)
    data_ts_corr = ts_corr(data['close'], data['vol'], 5)
    # 7. 计算 multiply(ts_returns(close, 20), ts_rank(divide(ts_std_dev(returns, 10), ts_std_dev(returns, 30)), 10), ts_corr(close, vol, 5))
    factor = multiply(data_ts_returns, data_ts_rank, data_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()