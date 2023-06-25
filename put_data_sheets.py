import os
import json
import pandas as pd
from utils.sheets import GoogleSheet

import logging

# Create logger
LOG = logging.getLogger("Put Data Sheets")
logging.basicConfig(level=logging.INFO)

LOG.info("Starting Extract Scandal Corruption Network")

from dotenv import load_dotenv
load_dotenv()
 
SPREADSHEET_ID = os.getenv("SPREADSHEET_ONTOLOGY")  # Links de Noticias
# Initialize Google Sheet
gsheet = GoogleSheet(SPREADSHEET_ID)

# iterate by filenames in data/processed_article
# lista los archivos crudos en la carpeta data/raw_article
list_files = os.listdir("data/processed_article")
# Filtra solo los archivos JSON
list_files = [file for file in list_files if file.endswith(".json")]
# Exclude files that start with _
list_files = [file for file in list_files if not file.startswith("_")]
# itera sobre los archivos

for filename in list_files:
    LOG.info("Processing file: %s", filename)

    try:
        LOG.info("Reading file: %s", filename)
        with open(f'data/processed_article/{filename}', "r", encoding="utf-8") as file:
            json_news = json.loads(file.read())
        LOG.info("Reading file extracted_entities : %s", filename)
        with open("data/extracted_entities/" + filename, "r", encoding="utf-8") as file:
            json_NER = json.loads(file.read())
        LOG.info("Reading file extracted_relations: %s", filename)
        with open("data/extracted_relations/" + filename, "r", encoding="utf-8") as file:
            json_ER = json.loads(file.read())

        escandalo = json_news['EscandaloDeCorrupcion']
        noticia_url = json_news['URL']

        # Save to Google Sheet Noticia
        df_noticia = pd.DataFrame([json_news])
        gsheet.add_csv_to_sheet(df_noticia, 'Noticia')

        # Save to Google Sheet Entities
        ## Individuo
        df_individuo = pd.DataFrame(json_NER['Individuos'])
        df_individuo['Escandalo'] = escandalo
        df_individuo['Noticia'] = noticia_url
        gsheet.add_csv_to_sheet(df_individuo, 'Individuo')

        ## Organización
        df_organizacion = pd.DataFrame(json_NER['Organizaciones'])
        df_organizacion['Escandalo'] = escandalo
        df_organizacion['Noticia'] = noticia_url
        gsheet.add_csv_to_sheet(df_organizacion, 'Organizacion')

        # Save to Google Sheet Relaciones
        # Append a la hoja Relaciones
        df_rel_ind_org = pd.DataFrame(json_NER['Relaciones'])
        df_rel_ind_org['Escandalo'] = escandalo
        df_rel_ind_org['Noticia'] = noticia_url
        gsheet.add_csv_to_sheet(df_rel_ind_org, 'Relaciones Ind-Org')

        # Relación Individuo Individuo
        df_rel_ind_ind = pd.DataFrame(json_ER['Relaciones'])
        df_rel_ind_ind['Escandalo'] = escandalo
        df_rel_ind_ind['Noticia'] = noticia_url
        gsheet.add_csv_to_sheet(df_rel_ind_ind, 'Relaciones Ind-Ind')

        # at the end move file to data/processed_article/escandalo_name
        # move file to data/processed_article/escandalo_name
        os.makedirs(f'data/processed_article/{escandalo}', exist_ok=True)
        with open("data/processed_article/" + f'{escandalo}/' + filename, "w", encoding="utf-8") as file:
            file.write(json.dumps(json_news))
            LOG.info("File saved in: %s", f'data/processed_article/{escandalo}/' + filename)

        # delete file from raw_article
        os.remove(f'data/processed_article/{filename}')
    except Exception as e:
        LOG.error("Error processing file: %s", filename)
        LOG.error(e)
        continue
