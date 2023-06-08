from utils.any_news_scrapper import NewsScraper, ParserNews
from utils.sheets import GoogleSheet
import numpy as np
import logging

# Create logger
LOG = logging.getLogger("NewsScraper")
logging.basicConfig(level=logging.INFO)

SPREADSHEET_ID = '1jc6qII2_ERr1mOE66WPT0vntL1xc7pT4Jupo3ef552k' # Links de Noticias
RANGE_NAME = 'Links!A1:E1000'

LOG.info("Starting NewsScraper")

# Inicio Servicios de Google 
gsheet = GoogleSheet(SPREADSHEET_ID)

# Lee los links de las noticias
df_links_raw = gsheet.read_sheet_to_df(RANGE_NAME)

#Nombres Columnas -> ['Nombre Entidad', 'Escandalo', 'Link', 'Relaciones Extraidas?']
# Filtra los links que ya fueron procesados
bool_mask = (df_links_raw['Relaciones Extraidas'] == 'TRUE') | (df_links_raw['Text Minado'] == 'TRUE')
df_links_to_process_raw = df_links_raw[~bool_mask]

# Filtra las filas que no tienen link, entidad o escandalo
# Si viene con un string vacio, se reemplaza por NaN
df_links_to_process_filtered = df_links_to_process_raw.replace('', np.nan)


df_links_to_process = df_links_to_process_filtered.dropna(subset=['Link', 'Nombre Entidad', 'Escandalo'])

for index, row in df_links_to_process.iterrows():
    
    
    url = row['Link']
    pagina = row['Nombre Entidad']
    escandalo = row['Escandalo']
    filename = url.split("/")[-1][:100]
    LOG.info("Processing row: %s", filename)
    
    pages_indicator = {
        "elcolombiano": {"html_tag": "div", "indicator": {"id": "articulo_"}},
        "eluniversal": {"html_tag": "div", "indicator": {"class": "paragraph"}},
        "eltiempo": {"html_tag": "div", "indicator": {"class": "articulo-contenido"}},
        "wikipedia": {"html_tag": "div", "indicator": {"class": "mw-parser-output"}},
        "RT": {"html_tag": "div", "indicator": {"class": "article__text"}},
    }
    
    indicator = pages_indicator.get(pagina, None)
    
    # Si no no existe la pagina debe continuar con el siguiente
    if indicator is None:
        LOG.warning("Page not found: %s", pagina)
        continue
    try:
        response = NewsScraper(url).get_news() # TODO Iniciar fuera del for
        parser = ParserNews(response)
        raw_text = parser.parse_page(indicator)
        # save file to txt
        with open("data/raw_article/"+pagina+filename+'.txt', "w", encoding="utf-8") as file:
            LOG.info("Saving file: %s", filename)
            file.write(raw_text)
    except Exception as e:
        LOG.error("Error processing row: %s", filename)
        LOG.error(e)
        continue

LOG.info("Finished NewsScraper")