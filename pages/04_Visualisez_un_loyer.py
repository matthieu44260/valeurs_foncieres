import streamlit as st
import duckdb

st.title("Recherchez le loyer d'un bien")
st.divider()

type_bien = st.selectbox(
        'Choisissez le type de bien',
        ['Maison', 'Appartement'],
        index=None,
        placeholder='Type de bien')

if type_bien:
    if type_bien == 'Maison':
        con = duckdb.connect(database="donnees_immo/loyer_maison.duckdb", read_only=False)
    if type_bien == 'Appartement':
        con = duckdb.connect(database="donnees_immo/loyer_appt.duckdb", read_only=False)

    query = ("SELECT * FROM table_donnees")
    df = con.execute(query).df()
    st.dataframe(df)
