import duckdb
import pandas as pd

#con = duckdb.connect(database="data/donnees.duckdb", read_only=False)
#
#donnees = pd.read_csv("data/donnee_immo.csv")
#donnees['date_vente'] = pd.to_datetime(donnees['date_vente'])
#
#con.execute("CREATE TABLE IF NOT EXISTS table_donnees AS SELECT * FROM donnees")
#
#con.close()

con = duckdb.connect(database="donnees_immo/vente_maison.duckdb", read_only=False)

donnees = pd.read_csv("data/data_vente_maison.csv")
donnees['date_vente'] = pd.to_datetime(donnees['date_vente'])

con.execute("CREATE TABLE IF NOT EXISTS table_donnees AS SELECT * FROM donnees")

con.close()

con = duckdb.connect(database="donnees_immo/vente_appt.duckdb", read_only=False)

donnees = pd.read_csv("data/data_vente_appt.csv")
donnees['date_vente'] = pd.to_datetime(donnees['date_vente'])

con.execute("CREATE TABLE IF NOT EXISTS table_donnees AS SELECT * FROM donnees")

con.close()

con = duckdb.connect(database="donnees_immo/vente_local.duckdb", read_only=False)

donnees = pd.read_csv("data/data_vente_local.csv")
donnees['date_vente'] = pd.to_datetime(donnees['date_vente'])

con.execute("CREATE TABLE IF NOT EXISTS table_donnees AS SELECT * FROM donnees")

con.close()
