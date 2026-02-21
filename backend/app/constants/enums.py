from enum import Enum

# Enums for services
class TrueProbabilityMethod(str, Enum):
    VIG_FREE_MEAN = "vig_free_mean"

DEFAULT_TP_METHOD = TrueProbabilityMethod.VIG_FREE_MEAN

class MarketPeriod(str, Enum):
    FULL_GAME = "full_game"

# Enums for APIs
class EVSortingMethod(str, Enum):
    EV_DESC = "ev_desc"
    EV_ASC = "ev_asc"
    EDGE_DESC = "edge_desc"
    EDGE_ASC = "edge_asc"
    START_TIME_ASC = "start_time_asc"
    START_TIME_DESC = "start_time_desc"
    PULLED_AT_DESC = "pulled_at_desc"
    PULLED_AT_ASC = "pulled_at_asc"

