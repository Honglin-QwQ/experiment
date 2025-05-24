import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev, divide

def factor_5702(data, **kwargs):
    """
    因子名称: PriceVolumeMomentumSkew_45028
    数学表达式: divide(ts_skewness(close, 15), ts_std_dev(vol, 20))
    中文描述: 该因子旨在捕捉价格动量的偏度与成交量波动性之间的关系。它首先计算过去15天收盘价的偏度（ts_skewness(close, 15)），这反映了价格分布的不对称性，正偏度可能表明价格上涨幅度大于下跌幅度，负偏度则相反。然后，计算过去20天成交量的标准差（ts_std_dev(vol, 20)），这代表了成交量的波动程度。最后，将价格偏度除以成交量标准差。该因子的创新点在于结合了价格的偏度（而非简单的变化）和成交量的波动性，通过比率的形式来衡量在不同成交量波动环境下，价格趋势的非对称性。高因子值可能表明在相对稳定的成交量波动下，价格呈现明显的正偏态，预示着潜在的上涨动量；低因子值可能表明在较高的成交量波动下，价格呈现负偏态或对称分布，预示着下跌风险或缺乏明确趋势。这可以用于识别那些价格上涨趋势更具持续性且成交量波动相对可控的股票。
    因子应用场景：
    1. 趋势识别：识别价格趋势的非对称性，判断上涨或下跌的潜力。
    2. 风险评估：结合成交量波动性，评估价格趋势的稳定性和风险。
    3. 选股策略：筛选价格上涨趋势更具持续性且成交量波动相对可控的股票。
    """
    # 1. 计算 ts_skewness(close, 15)
    data_ts_skewness_close = ts_skewness(data['close'], d = 15)
    # 2. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], d = 20)
    # 3. 计算 divide(ts_skewness(close, 15), ts_std_dev(vol, 20))
    factor = divide(data_ts_skewness_close, data_ts_std_dev_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()