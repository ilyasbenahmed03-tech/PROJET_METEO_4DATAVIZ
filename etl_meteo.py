import pandas as pd
import sqlalchemy
import os
import unicodedata

nom_fichier_local = "MENSQ_69_previous-1950-2024.csv"

# Configuration de la base de donnees avec le port 5433
db_config = {
    "drivername": "postgresql+psycopg2",
    "username": "data_user",
    "password": "data_password_2026",
    "host": "127.0.0.1",
    "port": 5433,
    "database": "meteo_analysis"
}

# Fonction simple pour enlever les accents des noms de stations
def clean_text(text):
    if pd.isna(text):
        return text
    normalized = unicodedata.normalize('NFKD', str(text))
    return "".join([c for c in normalized if not unicodedata.combining(c)]).encode('ascii', 'ignore').decode('utf-8')

def process_data():
    if not os.path.exists(nom_fichier_local):
        print("Erreur : Le fichier csv est introuvable")
        return

    # Etape 1 : Lecture du fichier csv local
    print("Lecture du fichier csv...")
    with open(nom_fichier_local, mode='r', encoding='cp1252', errors='replace') as f:
        df = pd.read_csv(f, sep=';')

    print("Fichier charge. Debut des transformations...")

    # Etape 2 : Selection et nettoyage des donnees
    columns_to_keep = ['NUM_POSTE', 'NOM_USUEL', 'AAAAMM', 'TN', 'TX', 'RR']
    df_filtered = df[[col for col in columns_to_keep if col in df.columns]].copy()

    # Nettoyage des noms des stations
    df_filtered['NOM_USUEL'] = df_filtered['NOM_USUEL'].apply(clean_text)
    df_filtered['CODE_DEPT'] = '69'

    # Conversion de la date
    df_filtered['DATE'] = pd.to_datetime(df_filtered['AAAAMM'].astype(str) + '01', format='%Y%m%d', errors='coerce')

    # Suppression des lignes vides sur les colonnes importantes
    df_final = df_filtered.dropna(subset=['TN', 'TX', 'DATE']).copy()

    print("Calcul des nouvelles colonnes...")

    # Creation des colonnes pour l annee et le mois
    df_final['ANNEE'] = df_final['DATE'].dt.year
    df_final['MOIS'] = df_final['DATE'].dt.month

    # Calcul de la temperature moyenne
    df_final['TM'] = (df_final['TN'] + df_final['TX']) / 2

    # Creation des indicateurs pour le gel et la chaleur
    df_final['NB_MOIS_GEL'] = (df_final['TN'] < 0).astype(int)
    df_final['NB_MOIS_CHALEUR'] = (df_final['TX'] >= 30).astype(int)

    # Organisation des colonnes avant l envoi en base
    ordered_columns = [
        'NUM_POSTE', 'NOM_USUEL', 'CODE_DEPT', 'DATE', 'ANNEE', 'MOIS',
        'TN', 'TX', 'TM', 'RR', 'NB_MOIS_GEL', 'NB_MOIS_CHALEUR'
    ]
    df_final = df_final[ordered_columns]

    # Etape 3 : Chargement vers la base PostgreSQL
    print("Connexion et envoi des donnees vers PostgreSQL...")
    try:
        connection_url = sqlalchemy.engine.url.URL.create(**db_config)
        engine = sqlalchemy.create_engine(connection_url, client_encoding='utf8')

        # Envoi des donnees dans la table finale
        df_final.to_sql('climat_mensuel_enrichi', engine, if_exists='replace', index=False)
        print("Sauvegarde reussie dans la base de donnees")
        print(f"Nombre de lignes envoyees : {len(df_final)}")
    except Exception as e:
        print("Erreur pendant l envoi en base :")
        print(e)

if __name__ == '__main__':
    process_data()