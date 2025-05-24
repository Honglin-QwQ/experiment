import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, ts_kurtosis

def factor_5939(data, **kwargs):
    """
    因子名称: Volatility_Kurtosis_Ratio_73442
    数学表达式: divide(ts_std_dev(low, 240), ts_kurtosis(volume, 66))
    中文描述: 该因子计算了低价的长期波动率（过去240天的标准差）与成交量的短期峰度（过去66天的峰度）之比。低价波动率反映了市场对下跌风险的长期评估，而成交量峰度则捕捉了短期内交易活动的极端集中程度。较高的比值可能表明在市场对下跌风险的长期担忧背景下，短期内出现了异常的交易量集中，这可能预示着市场情绪的剧烈波动或潜在的价格反转。该因子结合了长期价格波动和短期交易行为的异常性，具有创新性，可以用于识别潜在的市场拐点或风险事件。
    因子应用场景：
    1. 识别潜在的市场拐点或风险事件。
    2. 辅助判断市场情绪的剧烈波动。
    """
    # 1. 计算 ts_std_dev(low, 240)
    data_ts_std_dev_low = ts_std_dev(data['low'], 240)
    # 2. 计算 ts_kurtosis(volume, 66)
    data_ts_kurtosis_volume = ts_kurtosis(data['vol'], 66)
    # 3. 计算 divide(ts_std_dev(low, 240), ts_kurtosis(volume, 66))
    factor = divide(data_ts_std_dev_low, data_ts_kurtosis_volume)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()