import io
from dataclasses import dataclass
from enum import Enum
from pkgutil import get_data

import pandas as pd


class ReferenceMetric(Enum):
    """
    enum for reference metrics
    """

    POWER = 1
    WKG = 2


class PleasureIndex(Enum):
    """
    enum for pleasure index
    """

    EASY = 1, "Easy"
    MEDIUM = 2, "Medium"
    HARD = 3, "Hard"


@dataclass
class Options:
    riders: int = 8
    reference_metric: ReferenceMetric = ReferenceMetric.POWER
    target_turn_length: int = 30
    reference_power_scale = 3
    pleasure_index = PleasureIndex.MEDIUM

    def __post_init__(self):
        power_muliplier_data = get_data("tttcalculator", "data/power_multiplier.csv")
        self.power_multiplier_data = pd.read_csv(io.BytesIO(power_muliplier_data), index_col=0)
