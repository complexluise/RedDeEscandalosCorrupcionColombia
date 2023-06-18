import os
import json
import pandas as pd

from utils.llm_extract import extract_relations, extract_entities
from utils.sheets import GoogleSheet

import logging

# Create logger
LOG = logging.getLogger("ExtractRelationships")
logging.basicConfig(level=logging.INFO)

SPREADSHEET_ID = '1lnrxTIbBYYrMwodD7cEmolC7BQk1NVVrFjQiQon8tzQ'
# Initialize Google Sheet
gsheet = GoogleSheet(SPREADSHEET_ID)


# lista los archivos crudos en la carpeta data/raw_article
list_files = os.listdir("data/raw_article")
# elimina.desktop
#list_files.remove(".desktop")


# itera sobre los archivos

#for filename in list_files:
filename = list_files[0]
# open file and return text
path_file = f'data/raw_article/{filename}'
filename = path_file.split("/")[-1]

with open(path_file, "r", encoding="utf-8") as file:
    json_news = file.load()
    
    
## Ejemplo
input = {"article":json_news["content"]}

chat_completion_NER = extract_entities(input)

# save raw response
with open("data/extracted_entities/" + filename.replace("txt"), "w", encoding="utf-8") as file:
    file.write(chat_completion_NER["text"])

try:
    json_NER = json.loads(chat_completion_NER["text"])
except Exception as e:
    LOG.error(e)
    #continue
    

individuos = [item["Nombre"] for item in json_NER['Individuos']]
individuos = ', '.join(individuos)
individuos

input.update({"individuos": individuos})

chat_completion_ER = extract_relations(input)

# save raw response
with open("data/extracted_entities/" + filename.replace("txt"), "w", encoding="utf-8") as file:
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
