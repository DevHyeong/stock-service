from enum import Enum


class MarketType(str, Enum):
    ALL = "000"      # 전체
    KOSPI = "001"    # 코스피
    KOSDAQ = "101"   # 코스닥