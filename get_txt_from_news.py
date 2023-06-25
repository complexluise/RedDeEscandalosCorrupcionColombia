import json
import numpy as np
import logging

from utils.any_news_scrapper import NewsScraper, ParserNews
from utils.sheets import GoogleSheet
from utils.data_cleaning import replace_chars
# Create logger
LOG = logging.getLogger("NewsScraper")
logging.basicConfig(level=logging.INFO)

import os
from dotenv import load_dotenv
load_dotenv()

 
char_dict = {
    ":": "_",
    ',': "",
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "ñ": "n",
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "Ñ": "N",
    "¿": "",
    "?": "",
    "¡": "",
    "!": "",
    "(": "",
    ")": "",
    '"': "",
    "'": "",
    "“": "",
    "”": "",
    "|": "",
    "‘": "",
    "’": "",
}

SPREADSHEET_ID = os.getenv(SPREADSHEET_LINKS)  # Links de Noticias
RANGE_NAME = 'Links!A1:G1000'

LOG.info("Starting NewsScraper")

# Inicio Servicios de Google 
gsheet = GoogleSheet(SPREADSHEET_ID)

# Lee los links de las noticias
df_links_raw = gsheet.read_sheet_to_df(RANGE_NAME)

# Nombres Columnas -> ['Nombre Entidad', 'Escandalo', 'Link', 'Relaciones Extraidas?']
# Filtra los links que ya fueron procesados
bool_mask = (df_links_raw['Relaciones Extraidas'] == 'TRUE') | (df_links_raw['Text Minado'] == 'TRUE')
df_links_to_process_raw = df_links_raw[~bool_mask]

# Filtra las filas que no tienen link, entidad o escandalo
# Si viene con un string vacio, se reemplaza por NaN
df_links_to_process_filtered = df_links_to_process_raw.replace('', np.nan)

df_links_to_process = df_links_to_process_filtered.dropna(subset=['Fuente', 'Escandalo', 'Link', 'Titulo'])

for index, row in df_links_to_process.iterrows():

    item = {
        "Titulo": row['Titulo'],
        "Autor": '' if row['Autor'] is np.nan else row['Autor'],
        "URL": row['Link'],
        "EscandaloDeCorrupcion": row['Escandalo'],
        "Fuente": row['Fuente'],
    }

    filename = replace_chars(item['Titulo'], char_dict)
    LOG.info("Processing row: %s", filename)

    pages_indicator = {

        "asuntoslegales": {"html_tag": "div", "indicator": {"class": "postContent cell"}},
        "bluradio": {"html_tag": "div", "indicator": {"class": "RichTextArticleBody"}},
        "caracol": {"html_tag": "div", "indicator": {"class": "cnt-txt"}},
        "caracolradio": {"html_tag": "div", "indicator": {"class": "cnt-txt"}},
        "caracoltv": {"html_tag": "div", "indicator": {"class": "RichTextArticleBody-body RichTextBody"}},
        "elcolombiano": {"html_tag": "div", "indicator": {"class": "noticia"}},
        "elespectador": {"html_tag": "article"},
        "elpaís": {"html_tag": "div", "indicator": {"class": "paywall", "data-index": "0"}},
        "eltiempo": {"html_tag": "div", "indicator": {"class": "articulo-contenido"}},
        "eluniversal": {"html_tag": "div", "indicator": {"class": "paragraph"}},
        "lafm": {"html_tag": "div", "indicator": {"class": "column"}},
        "las2orillas": {"html_tag": "article", "indicator": {"id": "post-549866"}},
        "noticiasrcn": {"html_tag": "div", "indicator": {"class": "col-md-11 col-sm-12 text-note"}},
        # "wikipedia": {"html_tag": "div", "indicator": {"class": "mw-parser-output"}},
        "publimetro": {"html_tag": "article", "indicator": {"class": "default__ArticleBody-xb1qmn-2 dwgCRL article-body-wrapper"}},
        "portafolio": {"html_tag": "div", "indicator": {"class": "article-content"}},
        "semana": {"html_tag": "div", "indicator": {"class": "article-main"}},
        "radionacional": {"html_tag": "div", "indicator": {"class": "rnal_articulo_contenido_adicional container"}},
        "rtvc": {"html_tag": "div", "indicator": {"class": "mvp-content-wrap"}},

        "W Radio": {"html_tag": "article"},
    }

    normalice_fuente = item['Fuente'].replace(" ", "").lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")

    indicator = pages_indicator.get(normalice_fuente, None)

    # Si no no existe la pagina debe continuar con el siguiente
    if indicator is None:
        LOG.warning("Page not found: %s", item['Fuente'])
        continue
    try:
        response = NewsScraper(item['URL']).get_news()  # TODO Iniciar fuera del for
        parser = ParserNews(response)
        raw_text = parser.parse_page(indicator)
        item.update({"Contenido": raw_text})

        # save file to txt
        with open("data/raw_article/" + item['Fuente'] + "_" + filename + '.json', "w", encoding="utf-8") as file:
            LOG.info("Saving file: %s", item['Titulo'])
            file.write(json.dumps(item, indent=4, ensure_ascii=False))

    except Exception as e:
        LOG.error("Error processing row: %s", filename)
        LOG.error(e)
        continue

LOG.info("Finished NewsScraper")
