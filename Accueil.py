import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from couleurs import background_image


st.set_page_config(
        page_title="Valeurs foncières",
        layout="wide"
    )


#def local_css(file_name):
#    with open(file_name) as f:
#        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#
#local_css("theme.css")


def main():
    background_image('./images/image_accueil.jpg')
    a, b, c, d, e = st.columns(5)
    with c:
        st.markdown(" ")
        st.header('Valeurs foncières', divider='rainbow')
        st.markdown(" ")
    m, n, p = st.columns(3)
    with n:
        st.subheader("Sur cette application, vous pouvez :")
        st.markdown(" ")
        st.markdown(" ")
    f, g, h, i, j = st.columns(5)
    with f:
        if st.button("S'informer sur des biens vendus : ***Avoir des informations sur des biens déjà vendus, voir "
                     "l'état du marché, visualisez l'évolution des prix***"):
            switch_page("s'informer sur des biens vendus")
    with h:
        if st.button("Estimez la valeur de votre bien : ***Obtenir une estimation du prix d'un bien à partir de ses "
                     "caractéristiques***"):
            switch_page("estimez le prix d'un bien")
    with j:
        if st.button("Obtenir le loyer d'un logement : ***Trouver les loyers pratiqués dans une commune***"):
            switch_page("Obtenir le loyer d'un logement")

    for i in range(24):
        st.markdown("")
    st.markdown("<u>Source:</u> Ministère de l'Economie, des Finances et de la souveraineté industrielle et numérique.",
                unsafe_allow_html=True)
    st.markdown("Données originales téléchargées sur http://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/"
                ", mise à jour du 10 octobre 2023.")


if __name__ == "__main__":
    main()
