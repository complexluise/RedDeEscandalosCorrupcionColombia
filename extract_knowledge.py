import os
import json
import pandas as pd

from utils.llm_extract import extract_relations, extract_entities

import logging

# Create logger
LOG = logging.getLogger("ExtractRelationships")
logging.basicConfig(level=logging.INFO)

LOG.info("Starting Extract Scandal Corruption Network")

# lista los archivos crudos en la carpeta data/raw_article
list_files = os.listdir("data/raw_article")
# Filtra solo los archivos JSON
list_files = [file for file in list_files if file.endswith(".json")]

# itera sobre los archivos

for filename in list_files:

    # filename = list_files[0]
    LOG.info("Processing file: %s", filename)
    # open file and return text
    path_file = f'data/raw_article/{filename}'
    filename = path_file.split("/")[-1]

    with open(path_file, "r", encoding="utf-8") as file:
        json_news = json.load(file)

    ## Ejemplo
    input = {"article": json_news["Contenido"]}

    LOG.info("Extracting entities")
    try:
        chat_completion_NER = extract_entities(input)
    except Exception as e:
        LOG.error(e)
        LOG.info("Continuing with next file")
        continue
    # save raw response
    with open("data/extracted_entities/" + filename, "w", encoding="utf-8") as file:
        file.write(chat_completion_NER["text"])

    try:
        json_NER = json.loads(chat_completion_NER["text"])
    except Exception as e:
        LOG.error(e)
        LOG.info("Continuing with next file")
        # continue

    individuos = [item["Nombre"] for item in json_NER['Individuos']]
    individuos = ', '.join(individuos)
    individuos

    input.update({"individuos": individuos})

    LOG.info("Extracting relations")

    try:
        chat_completion_ER = extract_relations(input)
    except Exception as e:
        LOG.error(e)
        LOG.info("Continuing with next file")
        continue

    # save raw response
    with open("data/extracted_relations/" + filename, "w", encoding="utf-8") as file:
        file.write(chat_completion_ER["text"])

    # copy file a processed_article
    with open(f'data/processed_article/{filename}', "w", encoding="utf-8") as file:
        file.write(json.dumps(json_news))

    # delete file from raw_article
    os.remove(path_file)
