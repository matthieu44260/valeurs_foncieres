import duckdb
import pandas as pd

con = duckdb.connect(database="data/donnees.duckdb", read_only=False)

donnees = pd.read_csv("data/donnee_immo.csv")
donnees['date_vente'] = pd.to_datetime(donnees['date_vente'])

con.execute("CREATE TABLE IF NOT EXISTS table_donnees AS SELECT * FROM donnees")

con.close()
