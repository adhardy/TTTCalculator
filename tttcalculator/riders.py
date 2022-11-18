from dataclasses import dataclass
from typing import Optional

import numpy as np

from tttcalculator.utils import ReferenceMetric


@dataclass
class Rider:
    number: int
    name: Optional[str] = None
    weight: Optional[float] = None
    power: Optional[int] = None

    def _get_reference(
        self,
        average_power: float,
        reference_power_scale: int,
        reference: ReferenceMetric = ReferenceMetric.POWER,
    ) -> float:
        """
        Calculate the reference metric for a rider (WATTS or WKG)

        Calculated as:

        (power / average_power) ^ reference_power_scale

        Parameters
        ----------
        average_power : float
            Average power of the team
        reference : ReferenceMetric
            What to calculate the reference metric from.
        reference_power_scale : int, optional
            Power to raise the reference metric to, by default 3
        """

        self.validate_power()

        if reference == ReferenceMetric.POWER:
            reference_value = self.power
        elif reference == ReferenceMetric.WKG:
            reference_value = self.wkg
        else:
            raise ValueError("Invalid reference metric")

        return (reference_value / average_power) ** reference_power_scale

    def get_turn_length(
        self,
        average_power: float,
        target_turn_length: int,
        reference: ReferenceMetric,
        reference_power_scale: int,
    ) -> float:
        """
        Calculate the turn length for a rider

        Parameters
        ----------
        target_turn_length : int
            Target turn length

        Returns
        -------
        int
            Turn length
        """

        return (
            self._get_reference(
                average_power=average_power, reference=reference, reference_power_scale=reference_power_scale
            )
            * target_turn_length
        )

    @property
    def wkg(self) -> float:

        self.validate_weight()
        self.validate_power()

        return self.power / self.weight

    def validate(self, att: str):
        try:
            self.__getattribute__(f"validate_{att}")()
        except AttributeError:
            raise NotImplementedError(f"Validation for {att} not implemented")

    def validate_weight(self):
        if self.weight is None or self.weight <= 0.0:
            raise ValueError("Rider weight not set")

    def validate_power(self):
        if self.power is None or self.power <= 0:
            raise ValueError("Rider power not set")


class Riders:
    def __init__(
        self,
        num_riders: int,
    ):
        self.riders = [Rider(number=ii) for ii in range(num_riders)]

    def __getitem__(self, item):
        return self.riders[item]

    def __len__(self):
        return len(self.riders)

    def __iter__(self):
        return iter(self.riders)

    def __str__(self):
        str_ = "Riders:"
        for rider in self.riders:
            str_ += f"\n\t{rider}"

        return str_

    def get_rider_attribute(self, attr: str):
        return [getattr(rider, attr) for rider in self.riders]

    def average(self, attr: str):

        att_values = self.get_rider_attribute(attr)

        return np.average(att_values)

    def stddev(self, attr: str):

        att_values = self.get_rider_attribute(attr)

        return (
            np.std(att_values, ddof=1) / 2
        )  # ddof=1 for sample stddev (match excel), /2 matches the TTT original calculator

    def sec_average(self, attr: str):

        return self.average(attr) - self.stddev(attr)

    def stats(self, attr: str):

        return {
            "average": self.average(attr),
            "stddev": self.stddev(attr),
            "sec_average": self.sec_average(attr),
        }

    def validate(self, att: str):

        for rider in self.riders:
            rider.validate(att)

    def riders_with_data(self, attr: str):
        return [rider for rider in self.riders if getattr(rider, attr) is not None and getattr(rider, attr) > 0]

    def get_turn_lengths(
        self, reference_metric: ReferenceMetric, target_avg_turn_length: int, reference_power_scale: int
    ) -> list[float]:

        kwargs = {
            "average_power": self.average(reference_metric.name.lower()),
            "target_turn_length": target_avg_turn_length,
            "reference": reference_metric,
            "reference_power_scale": reference_power_scale,
        }

        return [rider.get_turn_length(**kwargs) for rider in self.riders]
