import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, log, ts_rank, multiply

def factor_5682(data, **kwargs):
    """
    因子名称: factor_innovative_vwap_low_delta_39295
    数学表达式: ts_delta(log(vwap), 5) * ts_rank(ts_delta(low, 5), 10)
    中文描述: 本因子结合了成交量加权平均价格（VWAP）的对数变化与最低价变化排名的概念，旨在捕捉价格和交易量之间的微妙关系。首先，计算VWAP的对数变化，这可以反映价格变化的幅度，并对极端值进行平滑处理。然后，计算最低价的5日变化，并对其进行排名，以衡量其相对强度。最后，将这两个因素相乘，旨在识别出在低价变化相对强势时，价格和交易量同步变化的模式。这种结合考虑了价格的波动和交易量的配合，可能有助于识别趋势的启动或反转点。本因子的创新之处在于将价格的对数变化与低价变化的排名相结合，从而更全面地反映了市场动态。
    因子应用场景：
    1. 趋势识别：识别价格和交易量同步变化的模式，可能有助于识别趋势的启动或反转点。
    2. 市场同步性分析：因子有助于识别市场中价格变化与收益率同步性较高的股票，这些股票可能对市场整体趋势更为敏感。
    """
    # 1. 计算 log(vwap)
    data['log_vwap'] = log(data['vwap'])
    
    # 2. 计算 ts_delta(log(vwap), 5)
    data['ts_delta_log_vwap'] = ts_delta(data['log_vwap'], 5)
    
    # 3. 计算 ts_delta(low, 5)
    data['ts_delta_low'] = ts_delta(data['low'], 5)
    
    # 4. 计算 ts_rank(ts_delta(low, 5), 10)
    data['ts_rank_ts_delta_low'] = ts_rank(data['ts_delta_low'], 10)
    
    # 5. 计算 ts_delta(log(vwap), 5) * ts_rank(ts_delta(low, 5), 10)
    factor = multiply(data['ts_delta_log_vwap'], data['ts_rank_ts_delta_low'])

    # 删除中间变量
    del data['log_vwap']
    del data['ts_delta_log_vwap']
    del data['ts_delta_low']
    del data['ts_rank_ts_delta_low']
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()