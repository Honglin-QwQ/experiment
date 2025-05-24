import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_mean, divide

def factor_5811(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(vwap, 10), ts_mean(vol, 120))
    中文描述: 该因子计算短期VWAP的标准差与长期成交量平均值的比率。VWAP的标准差衡量短期价格波动性，而长期成交量平均值反映市场长期活跃度。通过将短期价格波动性与长期市场活跃度相结合，该因子旨在识别在长期流动性充足的市场中，短期价格波动异常的股票。高因子值可能表明短期价格波动相对于长期市场参与度较高，这可能预示着潜在的交易机会或风险。该因子创新性地结合了参考因子中的VWAP（通过其标准差衡量波动性）和长期成交量平均值，并使用了除法运算符来构建比率，从而提供了一个新的视角来分析市场动态。
    因子应用场景：
    1. 波动性分析：用于识别相对于长期成交量，短期价格波动较大的股票。
    2. 交易信号：高因子值可能提示潜在的交易机会，尤其是在市场流动性充足的情况下。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 10)
    # 2. 计算 ts_mean(vol, 120)
    data_ts_mean_vol = ts_mean(data['vol'], 120)
    # 3. 计算 divide(ts_std_dev(vwap, 10), ts_mean(vol, 120))
    factor = divide(data_ts_std_dev_vwap, data_ts_mean_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()