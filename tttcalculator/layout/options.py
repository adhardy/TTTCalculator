import streamlit as st
from tttcalculator.utils import Options, ReferenceMetric, PleasureIndex


def options_layout():
    options = Options()

    st.header("Options")

    options.riders = st.number_input("Number of riders", value=options.riders)

    course_type = st.radio("Course Type", ["Flat (Watts)", "Hilly (Watts/kg)"])
    if course_type == "Flat (Watts)":
        options.reference_metric = ReferenceMetric.POWER
    else:
        options.reference_metric = ReferenceMetric.WKG

    options.pleasure_index = st.radio(
        "Pleasure Index", PleasureIndex, index=1, format_func=lambda x: f"{x.value[0]}: {x.value[1]}"
    )

    options.target_turn_length = st.number_input("Target turn length (seconds)", value=options.target_turn_length)

    with st.expander("Advanced"):
        options.reference_power_scale = st.number_input("Reference power scale", value=options.reference_power_scale)

    return options
