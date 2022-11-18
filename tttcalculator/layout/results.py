import streamlit as st
import numpy as np
import pandas as pd
from tttcalculator.riders import Riders
from tttcalculator.utils import ReferenceMetric, PleasureIndex
from typing import Callable
from collections import defaultdict

# pands: format float as .0f


def results_layout(
    riders: Riders,
    reference_metric: ReferenceMetric,
    reference_power_scale: int,
    target_turn_length: int,
    pleasure_index: PleasureIndex,
    power_multiplier_data: pd.DataFrame,
):

    _validate_metrics(riders, reference_metric)

    if reference_metric == ReferenceMetric.POWER:
        float_formatter = "{:.0f}".format
        power_unit = "Watts"

    else:
        float_formatter = "{:.1f}".format
        power_unit = "W/kg"

    ref_metric_name = reference_metric.name.lower()
    stats = riders.stats(ref_metric_name)
    turn_lengths = riders.get_turn_lengths(reference_metric, target_turn_length, reference_power_scale)

    cols = st.columns(2)

    _target_power(
        power_multiplier_data,
        pleasure_index,
        len(riders),
        float_formatter,
        power_unit,
        stats["average"],
        stats["sec_average"],
        cols[0],
    )

    _turn_lengths(turn_lengths, riders, float_formatter, reference_metric, power_unit, cols[1])

    _stats(
        stats,
        float_formatter,
        turn_lengths,
        power_unit,
    )


def _validate_metrics(riders: Riders, reference_metric: ReferenceMetric):

    try:
        riders.validate("power")
    except ValueError:
        st.error("Rider power not set")
        st.stop()

    if reference_metric == ReferenceMetric.WKG:
        try:
            riders.validate("weight")
        except ValueError:
            st.error("Rider weight not set")
            st.stop()


def _turn_lengths(
    turn_lengths: list[float],
    riders: Riders,
    float_formatter: Callable,
    reference_metric: ReferenceMetric,
    power_unit: str,
    st=st,
):
    st.header("Turn Lengths")

    # round turn lengths to nearest 5 seconds
    turn_lengths = [int(round(turn_length / 5) * 5) for turn_length in turn_lengths]
    st.caption("Target turn lengths for each rider, rounded to the nearest 5 seconds")

    turn_length_data = defaultdict(list)
    for rider, turn_length in zip(riders, turn_lengths):
        turn_length_data["Number"].append(rider.number + 1)
        turn_length_data["Rider"].append(rider.name)
        turn_length_data["Turn Length"].append(int(turn_length))
        turn_length_data[f"40 min. Power ({power_unit})"].append(
            float_formatter(getattr(rider, reference_metric.name.lower()))
        )

    df = pd.DataFrame(turn_length_data)
    df = df.set_index("Number")
    st.caption("Rider number:")
    st.table(df)


def _stats(stats: dict[str, float], float_formatter: Callable, turn_lengths: list[float], power_unit: str, st=st):

    st.header("Stats")

    st.write(f"Average turn length: {np.average(turn_lengths):.0f} seconds")

    rest_time_seconds = np.sum(turn_lengths) - np.average(turn_lengths)
    rest_time_str = f"{int(rest_time_seconds / 60)}min {int(rest_time_seconds % 60)}s"
    st.write(f"Rest time: {rest_time_str}")

    st.write(f"Average power: {float_formatter(stats['average'])} {power_unit}")


def _target_power(
    power_multiplier_data: pd.DataFrame,
    pleasure_index: PleasureIndex,
    num_riders: int,
    float_formatter: Callable,
    power_unit: str,
    average_power: float,
    second_average_power: float,
    st=st,
):
    st.header(f"Target {power_unit}")
    st.caption("Target power for the rider at the front of the group. As riders drop off, target power decreases.")

    # read the power multipluers csv and get the right column for the pleasure index
    power_multipliers = power_multiplier_data[f"{pleasure_index.value[0]}"]
    # select only rows where rider number is less than or equal to the number of riders
    power_multipliers = power_multipliers[power_multipliers.index <= num_riders]
    s_power_max = average_power * power_multipliers
    s_power_max.name = "Max"
    s_power_max = s_power_max.apply(float_formatter)
    s_power_min = second_average_power * power_multipliers
    s_power_min.name = "Min"
    s_power_min = s_power_min.apply(float_formatter)

    df_power = pd.merge(
        s_power_max,
        s_power_min,
        left_index=True,
        right_index=True,
    )
    st.caption("Riders remaining:")
    st.table(df_power)
