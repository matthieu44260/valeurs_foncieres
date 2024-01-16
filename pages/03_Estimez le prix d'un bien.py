import pandas as pd
import streamlit as st
import duckdb
from joblib import load

model_maison = load('./donnees_immo/model_maison.joblib')
preprocessor = load('./donnees_immo/preprocessor.joblib')

con = duckdb.connect(database="donnees_immo/donnees.duckdb", read_only=False)

st.header("Estimez le prix d'un bien en complétant les critères et appuyez sur Estimation")
st.divider()

code_postal_defaut = None
code_postal = None
sec_cad = None

col_a, col_b = st.columns(2)

with col_a:
    type_bien = st.selectbox(
            'Choisissez le type de bien',
            ['Maison', 'Appartement', 'Local'],
            index=None,
            placeholder='Type de bien'
        )
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

with col_b:
    department_choice = con.execute("SELECT DISTINCT num_departement FROM table_donnees ORDER BY num_departement").df()
    departement = st.selectbox(
        'Choisissez votre département',
        department_choice,
        index=None,
        placeholder='Département'
    )
    col_g, col_h, col_i = st.columns(3)
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
            with col_i:
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
        with col_h:
            code_postal = st.number_input(
                "Code postal",
                value=code_postal_defaut,
                min_value=0
            )


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
    df_nrm = preprocessor.transform(df)
    prix = int(model_maison.predict(df_nrm))
    st.subheader(f"Ce bien est estimé à :blue[{prix} €]")