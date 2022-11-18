import streamlit as st

from tttcalculator.layout.form import rider_form_layout
from tttcalculator.layout.options import options_layout
from tttcalculator.layout.results import results_layout
from tttcalculator.riders import Riders


def main():

    st.set_page_config(
        page_title="VCRT TTT Calculator",
        page_icon="resources/vcrt_favicon.jfif",
        initial_sidebar_state="expanded",
        layout="wide",
    )

    st.image("resources/vcrt.webp", width=200)
    st.title("TTT Calculator")

    with st.sidebar:
        options = options_layout()

    riders = Riders(options.riders)

    # store if the submit button has been clicked at least once this session
    # this is used to determine if the results should be displayed

    form_submitted = rider_form_layout(riders)

    if "form_submitted" not in st.session_state:
        st.session_state["form_submitted"] = form_submitted
    else:
        st.session_state["form_submitted"] = st.session_state["form_submitted"] or form_submitted

    if not st.session_state["form_submitted"]:
        # don't try to display results if the form hasn't been submitted this session
        st.stop()

    results_layout(
        riders=riders,
        reference_metric=options.reference_metric,
        reference_power_scale=options.reference_power_scale,
        target_turn_length=options.target_turn_length,
        pleasure_index=options.pleasure_index,
        power_multiplier_data=options.power_multiplier_data,
    )


if __name__ == "__main__":
    main()
