import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_rank, divide, ts_delay, ts_min

def factor_5600(data, **kwargs):
    """
    因子名称: factor_0002_32053
    数学表达式: ts_delta(ts_rank(divide(close,ts_delay(ts_min(low,d=5),222)),d=10),2)
    中文描述: 该因子是对历史因子factor_0001的改进，旨在捕捉长期低点支撑下的短期价格动量变化，并增强对异常低价的适应性。相较于直接使用low，这里使用了过去5天最低价的最小值ts_min(low,d=5)，然后将其延迟222天。这样做可以平滑短期低价的波动，减少异常低价对因子的影响，从而更稳定地反映长期支撑位的变化。通过这种方式，该因子试图识别更可靠的反转或趋势延续信号。
    因子应用场景：
    1. 趋势反转识别：当因子值显著变化时，可能预示着价格趋势的反转。
    2. 长期支撑位确认：结合历史数据，验证因子值与长期支撑位的关系，辅助判断支撑位的有效性。
    3. 异常低价过滤：通过平滑短期低价波动，提高因子对真实市场信号的敏感度。
    """
    # 1. 计算 ts_min(low,d=5)
    data['ts_min_low'] = ts_min(data['low'], d=5)
    
    # 2. 计算 ts_delay(ts_min(low,d=5),222)
    data['ts_delay_ts_min_low'] = ts_delay(data['ts_min_low'], d=222)
    
    # 3. 计算 divide(close,ts_delay(ts_min(low,d=5),222))
    data['divide_close_ts_delay_ts_min_low'] = divide(data['close'], data['ts_delay_ts_min_low'])
    
    # 4. 计算 ts_rank(divide(close,ts_delay(ts_min(low,d=5),222)),d=10)
    data['ts_rank_divide_close_ts_delay_ts_min_low'] = ts_rank(data['divide_close_ts_delay_ts_min_low'], d=10)
    
    # 5. 计算 ts_delta(ts_rank(divide(close,ts_delay(ts_min(low,d=5),222)),d=10),2)
    factor = ts_delta(data['ts_rank_divide_close_ts_delay_ts_min_low'], d=2)

    # 删除中间变量
    del data['ts_min_low']
    del data['ts_delay_ts_min_low']
    del data['divide_close_ts_delay_ts_min_low']
    del data['ts_rank_divide_close_ts_delay_ts_min_low']
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()