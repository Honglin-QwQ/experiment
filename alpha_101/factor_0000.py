import inspect
from operators import rank, ts_std_dev, signed_power, ts_arg_max
import pandas as pd

def factor_0000(data, **kwargs):
    """
    数学表达式: (rank(ts_arg_max(signed_power(((returns < 0) ? ts_std_dev(returns, 20) : close), 2.), 5)) - 0.5)
    中文描述: 该因子首先计算如果收益小于0，则取过去20天收益的标准差，否则取收盘价，然后对这个结果求平方，接着找到过去5天这个值最大的那一天是第几天，再计算这个天数排名的百分比，最后减去0.5。这个因子可能捕捉了下跌波动率和价格之间的关系，并试图找到短期内这种关系最强的时点。
    因子应用场景：
    1. 可以用于构建动量反转策略，当因子值较高时，可能意味着短期内下跌波动率较高，价格也较高，可能存在反转机会。
    2. 可以作为其他量化模型的输入特征，帮助模型识别市场状态和预测未来收益。
    3. 可以用于风险管理，当因子值较高时，可能意味着市场波动较大，需要调整仓位。
    """
    # 1. 计算 (returns < 0) ? ts_std_dev(returns, 20) : close
    std_dev_returns = ts_std_dev(data['returns'], 20)
    data['conditional_value'] = data.apply(lambda row: std_dev_returns[row.name] if row['returns'] < 0 else row['close'], axis=1)

    # 2. 计算 signed_power(((returns < 0) ? ts_std_dev(returns, 20) : close), 2.)
    data['signed_power_value'] = signed_power(data['conditional_value'], 2.)

    # 3. 计算 ts_arg_max(signed_power(((returns < 0) ? ts_std_dev(returns, 20) : close), 2.), 5)
    data['ts_arg_max_value'] = ts_arg_max(data['signed_power_value'], 5)

    # 4. 计算 rank(ts_arg_max(signed_power(((returns < 0) ? ts_std_dev(returns, 20) : close), 2.), 5))
    factor = rank(data['ts_arg_max_value'], 2)

    # 5. 计算 (rank(ts_arg_max(signed_power(((returns < 0) ? ts_std_dev(returns, 20) : close), 2.), 5)) - 0.5)
    factor = factor - 0.5

    # 删除中间变量
    del data['conditional_value']
    del data['signed_power_value']
    del data['ts_arg_max_value']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()
