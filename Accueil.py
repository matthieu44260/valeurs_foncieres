import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from couleurs import color_sidebar, background_image


st.set_page_config(
        page_title="Valeurs foncières",
        layout="wide"
    )


#def local_css(file_name):
#    with open(file_name) as f:
#        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#
## Utilisez la fonction local_css() pour inclure le fichier CSS
#local_css("theme.css")


def main():
    background_image('./images/image_accueil.jpg')
    color_sidebar()
    a, b, c, d, e = st.columns(5)
    with c:
        st.header('Valeurs foncières', divider='rainbow')
        st.markdown(" ")
    m, n, p = st.columns(3)
    with n:
        st.subheader("Avec cette application, vous pouvez :")
        st.markdown(" ")
    f, g, h, i, j = st.columns(5)
    with f:
        st.markdown("<span style='font-size:24px;'>:violet[***Avoir des informations sur des biens déjà vendus, voir "
                    "l'état du marché, visualisez l'évolution des prix***]</span>", unsafe_allow_html=True)
        st.markdown(" ")
        if st.button("S'informer sur des biens vendus"):
            switch_page("s'informer sur des biens vendus")
    with h:
        st.markdown("<span style='font-size:24px;'>:violet[***Obtenir une estimation du prix d'un bien à partir de ses"
                    " caractéristiques***]</span>", unsafe_allow_html=True)
        st.markdown(" ")
        if st.button("Estimez le prix d'un bien"):
            switch_page("estimez le prix d'un bien")
    with j:
        st.markdown("<span style='font-size:24px;'>:violet[***Trouver les loyers pratiqués dans une commune***]</span>",
                    unsafe_allow_html=True)
        st.markdown(" ")
        if st.button("Obtenir le loyer d'un logement"):
            switch_page("Obtenir le loyer d'un logement")
    for i in range(16):
        st.markdown("")
    st.markdown("<u>Source:</u> Ministère de l'Economie, des Finances et de la souveraineté industrielle et numérique.",
                unsafe_allow_html=True)
    st.markdown("Données originales téléchargées sur http://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/"
                ", mise à jour du 10 octobre 2023.")


if __name__ == "__main__":
    main()
