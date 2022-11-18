from dataclasses import dataclass
from enum import Enum


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

    EASY = 1, "I'm a pussy", 1.25
    MEDIUM = 2, "Go on then", 1.3
    HARD = 3, "Come at me bro", 1.35


@dataclass
class Options:
    riders: int = 8
    reference_metric: ReferenceMetric = ReferenceMetric.POWER
    target_turn_length: int = 30
    reference_power_scale = 3
    pleasure_index = PleasureIndex.MEDIUM
