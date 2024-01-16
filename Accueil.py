import streamlit as st
import os
import logging

#if "data" not in os.listdir():
#    logging.error(os.listdir())
#    logging.error("création du fichier data")
#    os.mkdir("data")
#
#if "donnees.duckdb" not in os.listdir("data"):
#    exec(open("init_all_db.py").read())

st.set_page_config(
        page_title="Valeurs foncières",
        layout="wide"
    )


def main():
    a, b, c, d, e = st.columns(5)
    with c:
        st.header('Valeurs foncières', divider='rainbow')
    f, g, h = st.columns(3)
    with g:
        st.caption("Trouver des informations sur des biens vendus ou estimer le prix d'un bien")


if __name__ == "__main__":
    main()
