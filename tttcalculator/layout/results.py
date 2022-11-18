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

    pleasure_factor = pleasure_index.value[2]
    power_min = pleasure_factor * stats["average"]
    power_max = pleasure_factor * stats["sec_average"]

    cols = st.columns(2)

    _target_power(
        power_min,
        power_max,
        float_formatter,
        power_unit,
        cols[0],
    )

    _turn_lengths(turn_lengths, riders, cols[1])

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
    st=st,
):

    st.header("Turn Lengths")
    turn_length_data = defaultdict(list)
    for rider, turn_length in zip(riders, turn_lengths):
        turn_length_data["Number"].append(rider.number + 1)
        turn_length_data["Rider"].append(rider.name)
        turn_length_data["Turn Length"].append(int(turn_length))

    df = pd.DataFrame(turn_length_data)
    df = df.set_index("Number")
    st.table(df)


def _stats(stats: dict[str, float], float_formatter: Callable, turn_lengths: list[float], power_unit: str, st=st):

    st.header("Stats")

    st.write(f"Average power: {float_formatter(stats['average'])} {power_unit}")
    st.write(f"Average turn length: {np.average(turn_lengths):.0f} seconds")

    rest_time_seconds = np.sum(turn_lengths) - np.average(turn_lengths)
    rest_time_str = f"{int(rest_time_seconds / 60)}min {int(rest_time_seconds % 60)}s"
    st.write(f"Rest time: {rest_time_str}")


def _target_power(
    power_min: float,
    power_max: float,
    float_formatter: Callable,
    power_unit: str,
    st=st,
):
    st.header(f"Target {power_unit}")
    st.write(f"Min: {float_formatter(power_min)}")
    st.write(f"Max: {float_formatter(power_max)}")
