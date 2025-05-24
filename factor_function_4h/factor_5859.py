import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, divide, multiply, rank

def factor_5859(data, **kwargs):
    """
    数学表达式: rank(multiply(divide(ts_std_dev(vwap, 5), ts_std_dev(vwap, 30)), ts_delta(vwap, 3)))
    中文描述: 该因子旨在捕捉短期波动率与长期波动率之比和短期动量之间的交互作用，并对结果进行排名。它首先计算VWAP在过去5天的标准差，并除以VWAP在过去30天的标准差，得到短期波动率相对于长期波动率的比例。然后，将这个比例与VWAP在过去3天的变化量（动量）相乘。最后，对乘积结果进行全市场排名。这个因子结合了参考因子中的ts_std_dev和ts_delta，并通过乘法操作符将波动率比率和动量结合，试图找到波动率和价格趋势共同作用下的交易机会。排名操作符用于增强因子的鲁棒性和可比性。较高的因子值可能表明短期波动率相对较高且价格呈现上涨动量，反之亦然。这个因子根据历史评估结果的改进建议，调整了时间窗口，并引入了ts_delta操作符来捕捉动量信息，通过乘法操作符结合了波动率和动量，并保留了rank操作符进行优化。
    因子应用场景：
    1. 波动率与动量结合：寻找短期波动率较高且价格呈现上涨动量的股票。
    2. 趋势识别：辅助识别波动率变化与价格趋势同步的股票，可能预示潜在的交易机会。
    """
    # 1. 计算 ts_std_dev(vwap, 5)
    data_ts_std_dev_short = ts_std_dev(data['vwap'], 5)
    # 2. 计算 ts_std_dev(vwap, 30)
    data_ts_std_dev_long = ts_std_dev(data['vwap'], 30)
    # 3. 计算 divide(ts_std_dev(vwap, 5), ts_std_dev(vwap, 30))
    data_divide = divide(data_ts_std_dev_short, data_ts_std_dev_long)
    # 4. 计算 ts_delta(vwap, 3)
    data_ts_delta = ts_delta(data['vwap'], 3)
    # 5. 计算 multiply(divide(ts_std_dev(vwap, 5), ts_std_dev(vwap, 30)), ts_delta(vwap, 3))
    data_multiply = multiply(data_divide, data_ts_delta)
    # 6. 计算 rank(multiply(divide(ts_std_dev(vwap, 5), ts_std_dev(vwap, 30)), ts_delta(vwap, 3)))
    factor = rank(data_multiply, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()