import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, log, divide, abs, ts_delta, multiply, floor

def factor_6003(data, **kwargs):
    """
    因子名称: Vol_High_Floor_Momentum_Ratio_87551
    数学表达式: divide(ts_std_dev(log(vol), 66), abs(ts_delta(multiply(high, floor(high)), 2)))
    中文描述: 该因子结合了交易量波动率和价格动量信息。它计算过去66天交易量对数标准差，并除以两天前最高价与其地板值乘积的绝对差。因子值越高，可能表明交易量波动较大，且价格动量较弱，可用于识别潜在的市场情绪变化或动量反转机会。
    因子应用场景：
    1. 识别市场情绪变化：当因子值较高时，可能表明市场情绪不稳定，交易量波动较大。
    2. 动量反转机会：因子值越高，可能意味着价格动量较弱，存在反转的可能性。
    """
    # 1. 计算 log(vol)
    data['log_vol'] = log(data['vol'])
    
    # 2. 计算 ts_std_dev(log(vol), 66)
    data['vol_std'] = ts_std_dev(data['log_vol'], d=66)
    
    # 3. 计算 floor(high)
    data['floor_high'] = floor(data['high'])
    
    # 4. 计算 multiply(high, floor(high))
    data['high_floor'] = multiply(data['high'], data['floor_high'])
    
    # 5. 计算 ts_delta(multiply(high, floor(high)), 2)
    data['high_floor_delta'] = ts_delta(data['high_floor'], d=2)
    
    # 6. 计算 abs(ts_delta(multiply(high, floor(high)), 2))
    data['abs_high_floor_delta'] = abs(data['high_floor_delta'])
    
    # 7. 计算 divide(ts_std_dev(log(vol), 66), abs(ts_delta(multiply(high, floor(high)), 2)))
    factor = divide(data['vol_std'], data['abs_high_floor_delta'])

    # 删除中间变量
    del data['log_vol']
    del data['vol_std']
    del data['floor_high']
    del data['high_floor']
    del data['high_floor_delta']
    del data['abs_high_floor_delta']
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()