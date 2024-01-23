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
    m, n, p = st.columns(3)
    with n:
        st.subheader("Sur notre application, vous pouvez :")
        st.markdown(" ")
    f, g, h, i, j = st.columns(5)
    with f:
        st.markdown("<span style='font-size:20px;'>Avoir des informations sur des biens déjà vendus, "
                    "voir l'état du marché, visualisez l'évolution des prix</span>", unsafe_allow_html=True)
        st.markdown(" ")
        if st.button("S'informer sur des biens vendus"):
            switch_page("s'informer sur des biens vendus")
    with h:
        st.markdown("<span style='font-size:20px;'>Obtenir une estimation du prix d'un bien à partir de ses "
                    "caractéristiques</span>", unsafe_allow_html=True)
        st.markdown(" ")
        if st.button("Estimez le prix d'un bien"):
            switch_page("estimez le prix d'un bien")
    with j:
        st.markdown("<span style='font-size:20px;'>Trouver les loyers pratiqués dans une commune</span>",
                    unsafe_allow_html=True)
        st.markdown(" ")
        if st.button("Estimez le loyer d'un logement"):
            switch_page("visualisez un loyer")


if __name__ == "__main__":
    main()
