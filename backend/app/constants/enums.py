from enum import Enum


class TrueProbabilityMethod(str, Enum):
    VIG_FREE_MEAN = "vig_free_mean"

DEFAULT_TP_METHOD = TrueProbabilityMethod.VIG_FREE_MEAN


class MarketPeriod(str, Enum):
    FULL_GAME = "full_game"
