import streamlit as st
from streamlit_nej_datepicker import datepicker_component, Config
import jdatetime


def main():
    st.title("NEJ Streamlit Datepicker Demo")

    # Add your configuration here
    config = Config(dark_mode=True, locale="en", disabled_days=[jdatetime.date.today()], color_primary="#ff4b4b",
                    color_primary_light="#ff9494", selection_mode="range")

    result = datepicker_component(config=config)

    if st.button('Print Result'):
        st.write(result)


if __name__ == "__main__":
    main()
