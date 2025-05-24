import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, adv
import pandas as pd

def factor_5947(data, **kwargs):
    """
    因子名称: VWAP_Volume_Volatility_Ratio_99746
    数学表达式: divide(ts_std_dev(divide(vwap, close), 5), ts_std_dev(divide(volume, adv(volume, 20)), 10))
    中文描述: 该因子计算过去5天VWAP/收盘价比值的标准差与过去10天成交量/20天平均成交量比值的标准差的比值。参考了divide, ts_std_dev, adv运算符，以及vwap, close和volume数据。创新点在于：1. 引入了VWAP与收盘价的比值，捕捉日内交易均价与收盘价的相对关系，可能反映日内交易的强度和趋势。2. 引入了成交量与长期平均成交量的比值，衡量当前交易量的相对活跃度。3. 计算这两个比值的短期和中期波动性（标准差），并取其比值，旨在捕捉价格波动与成交量波动之间的相对强度关系。这可能用于识别在不同波动环境下，价格变动是否得到成交量的有效支撑或证伪。改进方向上，根据评估建议，我们使用了标准差（ts_std_dev）来衡量波动性，并尝试了不同的时间窗口（5和10），以捕捉不同时间尺度的波动特征。同时，通过比率结构，我们保留了历史输出中比较相对强度的思想，但替换了分子分母的计算逻辑，使其更侧重于波动性的比较。
    因子应用场景：
    1. 波动性分析：用于衡量价格波动与成交量波动之间的相对强度关系。
    2. 趋势识别：可能用于识别在不同波动环境下，价格变动是否得到成交量的有效支撑或证伪。
    """
    # 将'vol'重命名为'volume'
    data = data.rename(columns={'vol': 'volume'})
    # 1. 计算 vwap / close
    vwap_close_ratio = divide(data['vwap'], data['close'])
    # 2. 计算 ts_std_dev(vwap / close, 5)
    vwap_close_ratio_std = ts_std_dev(vwap_close_ratio, 5)
    # 3. 计算 adv(volume, 20)
    volume_adv = adv(data['volume'], 20)
    # 4. 计算 volume / adv(volume, 20)
    volume_adv_ratio = divide(data['volume'], volume_adv)
    # 5. 计算 ts_std_dev(volume / adv(volume, 20), 10)
    volume_adv_ratio_std = ts_std_dev(volume_adv_ratio, 10)
    # 6. 计算 divide(ts_std_dev(vwap / close, 5), ts_std_dev(volume / adv(volume, 20), 10))
    factor = divide(vwap_close_ratio_std, volume_adv_ratio_std)

    # 删除中间变量
    del data['volume']
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()