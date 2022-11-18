import streamlit as st

from tttcalculator.utils import Options, PleasureIndex, ReferenceMetric


def options_layout():
    options = Options()

    st.header("Options")

    options.riders = st.number_input("Number of riders:", value=options.riders, step=1, min_value=3, max_value=8)

    course_type = st.radio(
        "Course Type",
        ["Flat (Watts)", "Hilly (Watts/kg)"],
        help="Your speed on flat courses is mostly determined by pure Watts, on hilly courses your speed is more dependent on your power to weight ratio (Watts per kg).",  # noqa: E501
    )
    if course_type == "Flat (Watts)":
        options.reference_metric = ReferenceMetric.POWER
    else:
        options.reference_metric = ReferenceMetric.WKG

    options.pleasure_index = st.radio(
        "Pleasure Index",
        PleasureIndex,
        index=1,
        format_func=lambda x: f"{x.value[0]}: {x.value[1]}",
        help="Are you to race or just playing around? The higher the number the higher the watts.",
    )

    options.target_turn_length = st.number_input(
        "Target turn length (seconds)",
        value=options.target_turn_length,
        min_value=1,
        step=1,
        help="The target length of a turn in seconds. This is used to calculate the target turn length for each rider.",
    )

    with st.expander("Advanced"):
        options.reference_power_scale = st.number_input(
            "Reference power scale", value=options.reference_power_scale, help="I wouldn't..."
        )

    return options
