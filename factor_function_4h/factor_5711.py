import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev, divide

def factor_5711(data, **kwargs):
    """
    因子名称: PriceVolumeVolatilitySkew_88600
    数学表达式: divide(ts_skewness(close, 20), ts_std_dev(vol, 15))
    中文描述: 该因子旨在通过结合价格偏度与成交量波动率，识别市场中潜在的非对称风险或机会。它首先计算过去20天收盘价的偏度（ts_skewness(close, 20)），用于衡量价格分布的非对称性，正偏度表示价格有更多的小幅上涨和少量大幅下跌，负偏度则相反。接着，计算过去15天成交量的标准差（ts_std_dev(vol, 15)），反映成交量的波动程度。最后，将价格偏度除以成交量标准差。相较于参考因子，本因子调整了窗口期，并旨在通过价格偏度与成交量波动率的比值，更精细地捕捉在不同交易活跃度下价格趋势的非对称性。高因子值可能表明在相对稳定的成交量波动下，价格呈现明显的正偏态，预示潜在的上涨动能；低因子值可能表明在较高的成交量波动下，价格呈现负偏态或对称分布，预示下跌风险或缺乏明确趋势。这可以用于识别那些价格上涨趋势更具持续性且成交量波动相对可控的股票。
    因子应用场景：
    1. 识别非对称风险或机会：通过价格偏度和成交量波动率的结合，识别市场中潜在的非对称风险或机会。
    2. 捕捉价格趋势的非对称性：通过价格偏度与成交量波动率的比值，更精细地捕捉在不同交易活跃度下价格趋势的非对称性。
    3. 识别上涨动能：高因子值可能表明在相对稳定的成交量波动下，价格呈现明显的正偏态，预示潜在的上涨动能。
    4. 预示下跌风险：低因子值可能表明在较高的成交量波动下，价格呈现负偏态或对称分布，预示下跌风险或缺乏明确趋势。
    """
    # 1. 计算 ts_skewness(close, 20)
    data_ts_skewness = ts_skewness(data['close'], 20)
    # 2. 计算 ts_std_dev(vol, 15)
    data_ts_std_dev = ts_std_dev(data['vol'], 15)
    # 3. 计算 divide(ts_skewness(close, 20), ts_std_dev(vol, 15))
    factor = divide(data_ts_skewness, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()