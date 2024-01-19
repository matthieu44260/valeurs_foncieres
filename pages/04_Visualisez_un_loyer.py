import streamlit as st
import duckdb
from streamlit_extras.switch_page_button import switch_page

if st.button("Accueil"):
    switch_page("accueil")

st.title("Estimez le loyer d'un bien")
st.markdown("Estimations ANIL, à partir des données du Groupe SeLoger et de leboncoin")
st.divider()

calcul_loyer = None
commune = None

col_a, col_b, col_c = st.columns(3)
with col_a:
    type_bien = st.selectbox(
            'Choisissez le type de bien',
            ['Maison', 'Appartement'],
            index=None,
            placeholder='Type de bien'
    )

if type_bien:
    if type_bien == 'Maison':
        con = duckdb.connect(database="donnees_immo/loyer_maison.duckdb", read_only=True)
    if type_bien == 'Appartement':
        con = duckdb.connect(database="donnees_immo/loyer_appt.duckdb", read_only=True)
    department_choice = con.execute("SELECT DISTINCT DEP FROM table_donnees ORDER BY DEP").df()
    with col_b:
        departement = st.selectbox(
            'Choisissez votre département',
            department_choice,
            index=None,
            placeholder='Département'
        )

    if departement:
        city_choice = con.execute(f"SELECT DISTINCT commune FROM table_donnees WHERE DEP = '{departement}' "
                                  f"ORDER BY commune").df()
        with col_c:
            commune = st.selectbox(
                'Choisissez votre commune',
                city_choice,
                index=None,
                placeholder='Commune'
            )

if commune:
    df = con.execute(f"SELECT * FROM table_donnees WHERE DEP = '{departement}' AND commune = '{commune}'").df()
    fourchette_basse = con.execute(f"SELECT fourchette_basse_au_m2 FROM table_donnees WHERE DEP = '{departement}' "
                                   f"AND commune = '{commune}'").fetchone()[0]
    fourchette_haute = con.execute(f"SELECT fourchette_haute_au_m2 FROM table_donnees WHERE DEP = '{departement}' "
                                   f"AND commune = '{commune}'").fetchone()[0]
    st.markdown(" ")
    st.markdown(f"<span style='font-size:24px;'>Les loyers pour un bien ({type_bien}) dans la commune de {commune} "
                f"varient entre :blue[{fourchette_basse}] et :blue[{fourchette_haute}] € au m².</span>",
                unsafe_allow_html=True)
    st.markdown(" ")
    col_d, col_e, col_f = st.columns(3)
    with col_d:
        calcul_loyer = st.number_input(
            "Indiquez une surface en m²",
            min_value=0,
            value=None
        )

if calcul_loyer:
    loyer_bas = int(fourchette_basse*calcul_loyer)
    loyer_haut = int(fourchette_haute*calcul_loyer)
    st.markdown(f"<span style='font-size:24px;'>Pour une surface de {calcul_loyer} m², "
                f"les loyers varient entre :blue[{loyer_bas}] et :blue[{loyer_haut}] €.</span>",
                unsafe_allow_html=True)
