import importlib
import json
import os
import sys
import warnings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List, Optional, Any
import logging
from tqdm import tqdm

from experiment import path_dr


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
CODES = [
    "AAPL", "ADBE", "AMAT", "AMD", "AMZN", "ASML", "AVGO", "CMCSA", "COST", "CSCO",
    "GOOGL", "INTU", "META", "MSFT", "NFLX", "NVDA", "PEP", "QCOM", "TMUS", "TSLA"
]
INDUSTRY_MAP = {
    # 科技
    "AAPL": "Technology",
    "ADBE": "Technology",
    "MSFT": "Technology",
    "GOOGL": "Technology",
    "META": "Technology",
    "INTU": "Technology",
    "AMZN": "Technology",  # 尽管有零售业务，但常被归类为科技

    # 半导体
    "AMAT": "Semiconductor",
    "AMD": "Semiconductor",
    "ASML": "Semiconductor",
    "AVGO": "Semiconductor",
    "NVDA": "Semiconductor",
    "QCOM": "Semiconductor",

    # 通信/媒体
    "NFLX": "Communication",
    "CMCSA": "Communication",
    "TMUS": "Communication",
    "CSCO": "Communication",

    # 消费品/零售
    "COST": "Consumer",
    "PEP": "Consumer",

    # 其他
    "TSLA": "Discretionary"  # 消费者自主品牌/汽车
}


def get_stock_data(
        symbol: str,
        sdt: str = "19900101",
        edt: str = "20250301",
        data_dir: str = f"{path_dr}/experiment/nasdaq_stocks_data_top20",
) -> pd.DataFrame:
    """
    获取股票数据

    Args:
        symbol: 股票代码，例如 'AAPL'
        sdt: 起始日期，格式为 'YYYYMMDD'
        edt: 结束日期，格式为 'YYYYMMDD'
        data_dir: 数据目录

    Returns:
        DataFrame: 股票数据
    """
    try:
        # 构建文件路径
        file_path = os.path.join(data_dir, f"{symbol}.csv")

        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.warning(f"找不到股票数据文件: {file_path}")
            return pd.DataFrame()

        # 读取CSV文件

        df = pd.read_csv(file_path)
        df = df.sort_values(['symbol', 'dt'])
        df['returns'] = df['close'].pct_change(1)
        df.drop('return', axis=1, inplace=True)
        df['vwap'] = df['vwap'].fillna((df['close'] + df['open']) / 2)
        df['vol'] = df['vol'].fillna(0)
        df['amount'] = df['amount'].fillna((df['vwap'] * df['vol']) / 2)

        share_cols = ['total_share', 'free_share']
        for col in share_cols:
            df[col] = df.groupby('symbol')[col].transform(
                lambda x: x.ffill().bfill()
            )
        df['total_share'] = df['total_share'].fillna(0)
        df['free_share'] = df['free_share'].fillna(0)
        mask_no_shares = df['total_share'].isna() & df['total_mv'].notna()
        df.loc[mask_no_shares, 'total_share'] = (
                df.loc[mask_no_shares, 'total_mv'] / df.loc[mask_no_shares, 'close']
        )
        df['free_share'] = df['free_share'].fillna(df['total_share'] * 0.8)
        df['total_mv'] = df['total_mv'].fillna(df['close'] * df['total_share'])
        df['free_mv'] = df['free_mv'].fillna(df['close'] * df['free_share'])
        df['turnover_ratio'] = df['turnover_ratio'].fillna(
            pd.Series(
                np.where(df['free_share'] > 0,
                         df['vol'] / df['free_share'] * 100,
                         0),
                index=df.index
            )
        )
        df['turnover_ratio'] = df['turnover_ratio'].clip(0, 100)

        # 6.2 市值必须为正
        df['total_mv'] = df['total_mv'].clip(lower=0)
        df['free_mv'] = df['free_mv'].clip(lower=0)

        # 6.3 流通股本不能大于总股本
        df['free_share'] = np.minimum(df['free_share'], df['total_share'])
        df.fillna(0, inplace=True)
        # 确保所有必需的列都存在
        required_columns = [
            "dt", "symbol", "close", "open", "high", "low", "pre_close", "returns",
            "vol", "amount", "vwap", "turnover_ratio", "free_share", "total_share",
            "free_mv", "total_mv"
        ]

        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            logger.error(f"数据缺少必需列: {missing_cols}")
            return pd.DataFrame()

        # 转换日期格式
        df["dt"] = pd.to_datetime(df["dt"])

        df["industry"] = df["symbol"].apply(lambda x: INDUSTRY_MAP.get(x, "Other"))
        # 筛选日期范围
        start_date = pd.to_datetime(sdt)
        end_date = pd.to_datetime(edt)
        mask = (df["dt"] >= start_date) & (df["dt"] <= end_date)
        df = df[mask].copy()

        # 按日期排序
        df = df.sort_values("dt").reset_index(drop=True)

        return df

    except Exception as e:
        logger.exception(f"读取股票数据失败: {symbol}")
        return pd.DataFrame()
class FactorAnalyzer:
    """因子分析器类"""
    
    def __init__(self):
        """初始化因子分析器"""
        self.codes = CODES
        self.factors_history = []  # 存储历史因子

        
    def update_nxb(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        计算未来N个bar的收益率

        Args:
            df: 数据框
            **kwargs: 其他参数
                - copy: 是否复制数据框
                - nseq: 收益率周期序列
                - bp: 是否转换为基点

        Returns:
            pd.DataFrame: 更新后的数据框
        """
        if kwargs.get("copy", False):
            df = df.copy()
            
        # 检查必需列
        assert all(
            col in df.columns for col in ["dt", "symbol", "close"]
        ), "缺少必需列"
        
        # 数据预处理
        df["dt"] = pd.to_datetime(df["dt"])
        df = df.sort_values(["symbol","dt"]).reset_index(drop=True)
        
        # 计算多个周期的未来收益率
        nseq = kwargs.get("nseq", (1, 2, 3, 5, 8, 10, 13))
        for symbol, dfg in df.groupby("symbol"):
            for n in nseq:
                # 使用收益率数据计算未来收益
                dfg[f"n{n}b"] = dfg["close"].shift(-n)/dfg["close"]-1
                df.loc[dfg.index, f"n{n}b"] = dfg[f"n{n}b"].fillna(0)
                
                # 转换为基点值
                if kwargs.get("bp", False):
                    df[f"n{n}b"] *= 10000
                    
        return df

    def calculate_factor(self, factor_func):
        """
        计算因子值

        Args:
            factor_func: 因子计算函数

        Returns:
            pd.DataFrame: 包含因子值的数据框
        """
        # 验证因子函数

        rows = []
        for symbol in tqdm(self.codes, desc="计算因子", unit="只"):
            try:
                # 获取股票数据，训练集
                df = get_stock_data(
                    symbol, 
                    sdt="20220601",
                    edt="20250601"
                )


                # 检查数据量
                if len(df) < 300:
                    logger.warning(f"{symbol} 数据量不足")
                    continue

                rows.append(df)
                
            except Exception as e:
                logger.exception(f"读取数据失败：{symbol}: {e}")
                
        # 合并数据
        if not rows:
            return pd.DataFrame()
            
        dfk = pd.concat(rows)
        dfk = dfk.set_index(["symbol", "dt"]).sort_index()
        try:
            dfk = factor_func(dfk)


            # def zscore(x):
            #     mean = x.mean()
            #     std = x.std()
            #     if std == 0:
            #         return x * 0
            #     return (x - mean) / std
            # cols=[col for col in dfk.columns if col.startswith("F#")]
            # for col in cols:
            #     dfk[col] = dfk.groupby("dt")[col].transform
            dfk = dfk.sort_index()
            dfk = dfk.reset_index()

            # 处理异常值
            dfk = dfk.replace([np.inf, -np.inf], np.nan)
            dfk = dfk.fillna(0)
            dfk = self.update_nxb(dfk, nseq=(1, 2, 3, 5, 8, 10, 13), bp=False)
        except Exception as e:
            logger.exception(f"因子计算失败: {e}")
            return e


        # 计算未来收益率

        
        return dfk


    def ic(self,
           df: pd.DataFrame,
           y_col: str = "n1b",
           x_col: str = str,
           method: str = "pearson",
           **kwargs) -> Dict:
        """
        计算因子IC值

        Args:
            df: 数据框
            x_col: 因子列名
            y_col: 目标变量列名
            method: 相关系数计算方法
            **kwargs: 其他参数

        Returns:
            Dict: IC统计信息
        """

        dt_col = kwargs.pop("dt_col", "dt")
        tqdm.pandas(desc="计算IC值")

        # 按时间计算ICimport warnings
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=RuntimeWarning)

                # 按时间计算IC
            s = df.groupby(dt_col).progress_apply(
                    lambda row: row[x_col].corr(row[y_col], method=method)
            )

        df_ic = pd.DataFrame(s, columns=["ic"]).reset_index()

        # 初始化结果
        res = {
            "x_col": x_col,
            "y_col": y_col,
            "method": method,
            "ic_mean": 0,
            "ic_std": 0,
            "ic_ir": 0,
            "ic_win": 0,
            "ic_2%": 0
        }
        
        if df_ic.empty or len(df_ic) == 0:
            return res
            
        # 计算统计量
        df_ic = df_ic[~df_ic["ic"].isnull()].copy()
        ic_avg = df_ic["ic"].mean()
        ic_std = df_ic["ic"].std()
        if df_ic.empty or len(df_ic) == 0:
            return res
        res.update({
            "ic_mean": round(ic_avg, 4),
            "ic_std": round(ic_std, 4),
            "ic_ir": round(ic_avg / ic_std, 4) if ic_std != 0 else 0,
            "ic_win": round(len(df_ic[df_ic["ic"] * np.sign(ic_avg) > 0]) / len(df_ic), 4),
            "ic_2%": round(len(df_ic[df_ic["ic"].abs() > 0.02]) / len(df_ic), 4)
        })
        
        return res

    def correlation(self,
                   df: pd.DataFrame,
                   x_col: str,
                   y_col: str,
                   method: str = "pearson",
                   **kwargs) -> Dict:
        """
        计算两个因子的相关性

        Args:
            df: 数据框
            x_col: 第一个因子列名
            y_col: 第二个因子列名
            method: 相关系数计算方法
            **kwargs: 其他参数

        Returns:
            Dict: 相关性统计信息
        """
        dt_col = kwargs.pop("dt_col", "dt")
        tqdm.pandas(desc="计算相关性")

        # 按时间计算IC
        s = df.groupby(dt_col).progress_apply(
            lambda row: row[x_col].corr(row[y_col], method=method)
        )
        df_corr = pd.DataFrame(s, columns=["correlation"]).reset_index()

        
        # 计算统计量
        mean_corr = df_corr["correlation"].mean()
        std_corr = df_corr["correlation"].std()
        max_abs_corr = df_corr["correlation"].abs().max()
        
        return {
            "mean_correlation": mean_corr,
            "std_correlation": std_corr,
            "max_abs_corr": max_abs_corr
        }

    def verify_no_look_ahead(self,data,func,col):
        """验证因子是否有未来函数"""
        # 选择一个测试日期
        test_date = '2000-05-25'

        # 只使用截止到test_date的数据
        data1 = data[data.index.get_level_values('dt') <= test_date].copy()
        factor1 = func(data1)

        # 使用包含未来数据的完整数据
        factor2 = func(data.copy())

        # 比较test_date当天的因子值
        factor1_value = factor1.loc[factor1.index.get_level_values('dt') == test_date][col]
        factor2_value = factor2.loc[factor2.index.get_level_values('dt') == test_date][col]

        # 如果两者相等，说明没有未来函数
        if np.allclose(factor1_value, factor2_value, equal_nan=True):
            print("✅ 没有未来函数")
        else:
            print("❌ 存在未来函数")
if __name__ == "__main__":
    d='C:/Users/Administrator/PycharmProjects/factor_mining/alpha_101'

    f_a=FactorAnalyzer()
    n=0

    py_file = [f for f in os.listdir(d) if f.startswith('factor_0') and f>'factor_0100']
    for f in py_file[:]:
        module_path=f"alpha_101.{f[:-3]}"
        module=importlib.import_module(module_path)
        if hasattr(module, f[:-3]):
            func = getattr(module, f[:-3])
            df=f_a.calculate_factor(func)
            print(f_a.ic(df=df, x_col=f"F#{f[:-3]}#DEFAULT"))
            df.drop(f"F#{f[:-3]}#DEFAULT", axis=1, inplace=True)
            df.set_index(['symbol','dt'], inplace=True)
            print(f_a.verify_no_look_ahead(df, func,f"F#{f[:-3]}#DEFAULT"))

            print(n)
            n=n+1
