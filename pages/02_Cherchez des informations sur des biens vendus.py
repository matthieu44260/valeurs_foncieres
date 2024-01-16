import streamlit as st
import duckdb
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from typing import Union


st.header("Trouvez des informations sur les biens vendus des 5 dernières années")
st.divider()

con = duckdb.connect(database="donnees_immo/donnees.duckdb", read_only=False)


def get_coordinates(city: str, street: Union[str, None] = None):
    """
    Renvoie les coordonnées GPS en fonction des paramètres fournis
    """
    geolocator = Nominatim(user_agent="my_geocoder")
    if street:
        full_address = f"{street}, {city}, 'France'"
    else:
        full_address = f"{city}, 'France'"
    location = geolocator.geocode(full_address)
    return location


def calculate_prices(req: str) -> None:
    """
    Calcule et affiche la valeur moyenne et le prix au m² d'un bien selon le département, la commune et la rue
    :param req: la requête
    """
    mid_value = con.execute("SELECT MEAN(valeur_en_€)" + req).fetchone()[0]
    price_by_m = con.execute("SELECT SUM(valeur_en_€)/SUM(surface_bien)" + req).fetchone()[0]
    if mid_value and price_by_m:
        if type_bien == 'Maison':
            message = "d'une maison"
        else:
            message = f"d'un {type_bien.lower()}"
        st.write(f"Dans la zone sélectionée, le prix moyen {message} est de :blue[**{int(mid_value)} €**] "
                 f"et le prix moyen au m² est de :blue[**{int(price_by_m)} €**].")


def display_examples(req: str) -> None:
    """
    Affiche  les 5 derniers biens vendus
    :param req: la requête
    """
    features = ("type_local, CONCAT(YEAR(date_vente), '/', MONTH(date_vente), '/', DAY(date_vente)) AS date_de_vente, "
                "valeur_en_€, numero, CONCAT(type_voie, ' ', voie) AS voie, code_postal,"
                " commune, nbre_pieces, surface_bien, surface_terrain")
    req = "SELECT " + features + req
    properties = con.execute(req).df().sort_values('valeur_en_€', ascending=False)
    st.write(f"Voici une liste de {len(properties)} biens vendus dans la zone sélectionnée:")
    st.dataframe(properties, hide_index=True,
                 column_config={
                     "valeur_en_€": st.column_config.NumberColumn(format="%i"),
                     "code_postal": st.column_config.NumberColumn(format="%i"),
                     "surface_relle_bati": st.column_config.NumberColumn(format="%i"),
                     "surface_terrain": st.column_config.NumberColumn(format="%i"),
                     "numero": st.column_config.NumberColumn(format="%i")
                 }
                 )


def property_request(type_de_local: str, dep: int, com: str, rue: str) -> str:
    """
    Créer une fin de requête (sans le SELECT) selon les paramètres fournis en remplaçant la rue par sa zone cadastrale
    :param type_de_local: Maison ou Appartement ou local commercial
    :param dep: le département
    :param com: la commune
    :param rue: le nom de la rue
    :return: la fin de la requête (sans le select)
    """
    query = " FROM table_donnees"
    if departement:
        query = query + f" WHERE num_departement = '{dep}'"
        if commune:
            query = query + f" AND commune = '{com}'"
            if voie:
                sec_cad = con.execute("SELECT section" + query + f" AND voie = '{rue}'").fetchone()
                if sec_cad is not None:
                    sec_cad = sec_cad[0]
                    query = query + f" AND section = '{sec_cad}'"
        query = query + f" AND type_local = {type_de_local}"
        return query


def display_map(req: str) -> None:
    """
    Affiche la carte et des marqueurs en fonction de la rue choisie
    """
    if departement:
        coordinates = get_coordinates(departement*1000)
        zoom = 8
        if commune:
            coordinates = get_coordinates(commune)
            zoom = 13
            if voie:
                coordinates = get_coordinates(commune, voie)
                zoom = 16
        if coordinates:
            carte = folium.Map(location=[coordinates.latitude, coordinates.longitude], zoom_start=zoom)
            # Marker de la sélection
            (folium
             .Marker(location=[coordinates.latitude, coordinates.longitude], icon=folium.Icon(color="green"))
             .add_to(carte))
            # Marker des exemples
            if voie:
                streets = con.execute("SELECT DISTINCT(voie) " + req).fetchall()
                for i in range(min(5, len(streets))):
                    street = streets[i][0]
                    coord = get_coordinates(city=commune, street=street)
                    (folium
                     .Marker(location=[coord.latitude, coord.longitude], icon=folium.Icon(color="yellow"))
                     .add_to(carte))
            st_folium(carte)


def display_variations(query: str, col: str, titre: str) -> None:
    """
    Affiche l'évolution de la colonne col selon le departement, la ville et la zone cadastrale
    :param query: fin de requête
    :param col: colonne à afficher
    :param titre: titre du graphique à afficher
    """
    req_dep = (f"SELECT DATE_TRUNC('quarter', date_vente) AS periode, "
               f"MEAN({col}) AS prix_pour_le_departement FROM table_donnees "
               f"WHERE num_departement = '{departement}' GROUP BY periode ORDER BY periode")
    df = con.execute(req_dep).df()
    colors = ["#070b8f"]
    if commune:
        req_com = (f"SELECT DATE_TRUNC('quarter', date_vente) AS periode,"
                   f"MEAN({col}) AS prix_pour_la_commune FROM table_donnees WHERE num_departement = '{departement}'"
                   f"AND commune = '{commune}' GROUP BY periode ORDER BY periode")
        df_com = con.execute(req_com).df()
        df = duckdb.sql("SELECT * FROM df_com JOIN df USING(periode)").df()
        colors.append("#fc63ff")
    if voie:
        sec_cad = con.execute("SELECT section" + query).fetchone()
        if sec_cad is not None:
            sec_cad = sec_cad[0]
            req_zone = (f"SELECT DATE_TRUNC('quarter', date_vente) AS periode,"
                        f"MEAN({col}) AS prix_pour_le_quartier FROM table_donnees WHERE num_departement = '{departement}' "
                        f"AND commune = '{commune}' AND section = '{sec_cad}' GROUP BY periode ORDER BY periode")
            df_zone = con.execute(req_zone).df()
            df = duckdb.sql("SELECT * FROM df_zone JOIN df USING(periode)").df()
            colors.append("#fcd703")
    st.markdown(titre)
    st.line_chart(df, x='periode', color=colors, use_container_width=True)


def display_distributions(query: str) -> None:
    st.markdown(f"**Répartition des ventes selon le prix pour la commune de {commune}**")
    st.markdown('Choisissez la ou les années :')
    y1, y2, y3, y4, y5 = st.columns(5)
    with y1:
        year_2023 = st.checkbox('2023', value=True)
    with y2:
        year_2022 = st.checkbox('2022')
    with y3:
        year_2021 = st.checkbox('2021')
    #with y4:
    #    year_2020 = st.checkbox('2020')
    #with y5:
    #    year_2019 = st.checkbox('2019')
    years = []
    if year_2023:
        years.append(2023)
    if year_2022:
        years.append(2022)
    if year_2021:
        years.append(2021)
    #if year_2020:
    #    years.append(2020)
    #if year_2019:
    #    years.append(2019)
    valeurs = con.execute(f"SELECT valeur_en_€, YEAR(date_vente) as annee FROM table_donnees WHERE "
                          f"num_departement = '{departement}' AND commune = '{commune}' AND "
                          f"annee in {tuple(years)} AND valeur_en_€<=2000000").df()
    if valeurs.empty:
        st.markdown("Il n'y a aucun bien vendu dans cette commune sur la période choisie")
    elif valeurs.shape[0] == 1:
        st.markdown("Sélectionnez d'autres années")
    else:
        fig, ax = plt.subplots()
        sns.histplot(data=valeurs, x='valeur_en_€', bins=20, kde=True, log_scale=False, hue='annee',
                     multiple='dodge', palette='deep')
        ax = plt.gca()
        ax.xaxis.set_major_formatter('{x:,.0f}')
        plt.xticks(rotation=45)
        plt.xlabel("Valeur en €")
        plt.ylabel("Nombre de ventes")
        fig


def application(type_de_local: str, dep: int, com: str, rue: str) -> None:
    """
    fonction principale qui lance les fonctions d'affichage
    :param type_de_local: Maison, Appartement ou Local
    :param dep: departement
    :param com: commune
    :param rue: rue
    """
    req = property_request(type_de_local=type_de_local, dep=departement, com=commune, rue=voie)
    dis_map, dis_info = st.columns([0.35, 0.65])
    with dis_map:
        display_map(req)
    with dis_info:
        calculate_prices(req)
        display_examples(req)
    dis_var1, dis_var2 = st.columns(2)
    with dis_var1:
        display_variations(req, 'valeur_en_€', "**Evolution du prix moyen de vente**")
    with dis_var2:
        display_variations(req, 'valeur_en_€/surface_bien', "**Evolution du prix moyen au m²**")
    dis_distrib, dis_year = st.columns(2)
    with dis_distrib:
        if commune:
            display_distributions(req)


commune = ''
section = ''
voie = ''
with st.sidebar:
    type_bien = st.selectbox(
        'Choisissez le type de bien',
        ['Maison', 'Appartement', 'Local'],
        index=None,
        placeholder='Type de bien'
    )
    department_choice = con.execute("SELECT DISTINCT num_departement FROM table_donnees ORDER BY num_departement").df()
    departement = st.selectbox(
        'Choisissez votre département',
        department_choice,
        index=None,
        placeholder='Département'
    )
    if departement:
        city_choice = con.execute(f"SELECT DISTINCT commune FROM table_donnees WHERE num_departement = '{departement}'"
                                  f" ORDER BY commune").df()
        commune = st.selectbox(
            'Choisissez votre commune',
            city_choice,
            index=None,
            placeholder='Commune'
        )
    if commune:
        street_choice = con.execute(f"SELECT DISTINCT voie FROM table_donnees"
                                    f" WHERE num_departement = '{departement}' AND commune = '{commune}'"
                                    f" ORDER BY voie").df()
        voie = st.selectbox(
            'Choisissez un nom de rue',
            street_choice,
            index=None,
            placeholder='nom de rue'
        )

# Display prices and examples
if type_bien:
    if departement:
        application(type_de_local=f"'{type_bien}'", dep=departement, com=commune, rue=voie)
