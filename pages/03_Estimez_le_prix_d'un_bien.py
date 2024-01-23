import pandas as pd
import streamlit as st
import duckdb
from joblib import load
from streamlit_extras.switch_page_button import switch_page

preprocessor = load('./donnees_immo/preprocessor.joblib')

if st.button("Accueil"):
    switch_page("accueil")

st.header("Complétez les critères dont vous disposez et appuyez sur Estimation")
st.divider()

code_postal_defaut = None
code_postal = None
sec_cad = None
nbre_pieces = None
surface_bien = None
surface_terrain = None

col_a, col_b = st.columns(2)

with col_a:
    type_bien = st.selectbox(
            'Choisissez le type de bien',
            ['Maison', 'Appartement'],
            index=None,
            placeholder='Type de bien'
        )
    if type_bien == 'Maison':
        con = duckdb.connect(database="donnees_immo/vente_maison.duckdb", read_only=True)
        model = load('./donnees_immo/model_maison.joblib')
    if type_bien == 'Appartement':
        con = duckdb.connect(database="donnees_immo/vente_appt.duckdb", read_only=True)
        model = load('./donnees_immo/model_appt.joblib')
    if type_bien:
        col_d, col_e, col_f = st.columns(3)
        with col_d:
            nbre_pieces = st.number_input(
                "Nombre de pièces",
                min_value=0
            )
        with col_e:
            surface_bien = st.number_input(
                "Surface du bien en m²",
                min_value=0,
                value=None
            )
        with col_f:
            surface_terrain = st.number_input(
                "Surface du terrain en m²",
                value=0
            )

if type_bien:
    with col_b:
        department_choice = con.execute("SELECT DISTINCT num_departement FROM table_donnees ORDER BY num_departement").df()
        departement = st.selectbox(
            'Choisissez votre département',
            department_choice,
            index=None,
            placeholder='Département'
        )
        col_g, col_h = st.columns(2)
        if departement:
            with col_g:
                city_choice = con.execute(f"SELECT DISTINCT commune FROM table_donnees WHERE num_departement = '{departement}'"
                                          f" ORDER BY commune").df()
                commune = st.selectbox(
                    'Choisissez votre commune',
                    city_choice,
                    index=None,
                    placeholder='Commune'
                )
            if commune:
                with col_h:
                    street_choice = con.execute(f"SELECT DISTINCT voie FROM table_donnees "
                                                f"WHERE num_departement = '{departement}' AND commune = '{commune}' "
                                                f"ORDER BY voie").df()
                    voie = st.selectbox(
                        'Choisissez un nom de rue',
                        street_choice,
                        index=None,
                        placeholder='nom de rue'
                    )
                    code_postal_defaut = con.execute(f"SELECT DISTINCT(code_postal) FROM table_donnees WHERE "
                                              f"num_departement = '{departement}' AND commune = '{commune}'").fetchone()[0]
                    if voie:
                        sec_cad = con.execute(f"SELECT section FROM table_donnees WHERE num_departement = '{departement}' "
                                              f"AND commune = '{commune}' AND voie = '{voie}'").fetchone()
                        if sec_cad is not None:
                            sec_cad = sec_cad[0]


estimer = st.button(
    "Estimation"
)

df = pd.DataFrame({
    'code_postal': [code_postal],
    'section': [sec_cad],
    'nbre_pieces': [nbre_pieces],
    'surface_bien': [surface_bien],
    'surface_terrain': [surface_terrain]
})

if estimer:
    if type_bien and departement and commune:
        df_nrm = preprocessor.transform(df)
        prix = int(model.predict(df_nrm))
        prix_m2 = con.execute(f"SELECT SUM(valeur_en_€)/SUM(surface_bien) FROM table_donnees "
                              f"WHERE num_departement = '{departement}' AND commune = '{commune}'").fetchone()[0]
        if voie:
            sec_cad = con.execute(f"SELECT section FROM table_donnees WHERE num_departement = '{departement}' "
                                  f"AND commune = '{commune}' AND voie = '{voie}'").fetchone()
            if sec_cad is not None:
                sec_cad = sec_cad[0]
            prix_m2 = con.execute(f"SELECT SUM(valeur_en_€)/SUM(surface_bien) FROM table_donnees "
                                  f"WHERE num_departement = '{departement}' AND commune = '{commune}' "
                                  f"AND section = '{sec_cad}'").fetchone()[0]
        else:
            prix_m2 = con.execute(f"SELECT SUM(valeur_en_€)/SUM(surface_bien) FROM table_donnees WHERE "
                                  f"num_departement = '{departement}' AND commune = '{commune}'").fetchone()[0]
        if surface_bien:
            prix_calcule = int(prix_m2*surface_bien)
        else:
            prix_calcule = int(prix_m2*100)
        prix = int((int(prix) + 2 * prix_calcule) / 3)
        prix = int(prix/1000)
        prix_min = int(prix*0.97)*1000
        prix_max = int(prix*1.03)*1000
        prix_min = str("{:,}".format(prix_min)).replace(',', ' ')
        prix_max = str("{:,}".format(prix_max)).replace(',', ' ')
        st.subheader(f"Ce bien est estimé entre :blue[{prix_min}] et :blue[{prix_max}]")
    else:
        st.markdown("Complétez le type de bien, le département et la commune")