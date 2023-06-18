import os
import json
import pandas as pd

from utils.llm_extract import extract_relations, extract_entities
from utils.sheets import GoogleSheet

import logging

# Create logger
LOG = logging.getLogger("ExtractRelationships")
logging.basicConfig(level=logging.INFO)

LOG.info("Starting Extract Scandal Corruption Network")

SPREADSHEET_ID = '1lnrxTIbBYYrMwodD7cEmolC7BQk1NVVrFjQiQon8tzQ'
# Initialize Google Sheet
gsheet = GoogleSheet(SPREADSHEET_ID)


# lista los archivos crudos en la carpeta data/raw_article
list_files = os.listdir("data/raw_article")
# Filtra solo los archivos JSON
list_files = [file for file in list_files if file.endswith(".json")]


# itera sobre los archivos

#for filename in list_files:

filename = list_files[0]
LOG.info("Processing file: %s", filename)
# open file and return text
path_file = f'data/raw_article/{filename}'
filename = path_file.split("/")[-1]

with open(path_file, "r", encoding="utf-8") as file:
    json_news = json.load(file)
    
    
## Ejemplo
input = {"article":json_news["content"]}

LOG.info("Extracting entities")
chat_completion_NER = extract_entities(input)

# save raw response
with open("data/extracted_entities/" + filename, "w", encoding="utf-8") as file:
    file.write(chat_completion_NER["text"])

try:
    json_NER = json.loads(chat_completion_NER["text"])
except Exception as e:
    LOG.error(e)
    LOG.info("Continuing with next file")
    #continue
    

individuos = [item["Nombre"] for item in json_NER['Individuos']]
individuos = ', '.join(individuos)
individuos

input.update({"individuos": individuos})

LOG.info("Extracting relations")
chat_completion_ER = extract_relations(input)

# save raw response
with open("data/extracted_relations/" + filename, "w", encoding="utf-8") as file:
    file.write(chat_completion_ER["text"])

try:
    json_ER = json.loads(chat_completion_ER["text"])
except Exception as e:
    LOG.error(e)
    #continue
    
    
    



# Save to Google Sheet

# dataframe noticia
# Append a la hoja Noticia

# dataframe Fuente
# Append a la hoja Fuente

# dataframe CasoDeCorrupcion
# Append a la hoja CasoDeCorrupcion

# dataframe Individuo
# Append a la hoja Individuo

# dataframe Organización
# Append a la hoja Organización

# dataframe Relaciones
# Append a la hoja Relaciones



# Añade a la hoja de cálculo de Google
#gsheet.add_csv_to_sheet(df, 'gpt')
