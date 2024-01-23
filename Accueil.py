import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
        page_title="Valeurs foncières",
        layout="wide"
    )


def main():
    a, b, c, d, e = st.columns(5)
    with c:
        st.header('Valeurs foncières', divider='rainbow')
        st.markdown(" ")
        st.markdown(" ")
    f, g, h, i, j = st.columns(5)
    with f:
        if st.button("S'informer sur des biens vendus"):
            switch_page("s'informer sur des biens vendus")
    with h:
        if st.button("Estimez le prix d'un bien"):
            switch_page("estimez le prix d'un bien")
    with j:
        if st.button("Estimez le loyer d'un logement"):
            switch_page("visualisez un loyer")


if __name__ == "__main__":
    main()
