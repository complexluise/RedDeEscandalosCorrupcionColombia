from utils.any_news_scrapper import NewsScraper, ParserNews
from utils.sheets import GoogleSheet

SPREADSHEET_ID = '1jc6qII2_ERr1mOE66WPT0vntL1xc7pT4Jupo3ef552k' # Links de Noticias
RANGE_NAME = 'Links!A1:C1000'



GoogleSheet

pages_indicator = {
    "elcolombiano": {"html_tag": "div", "indicator": {"id": "articulo_"}},
    "eluniversal": {"html_tag": "div", "indicator": {"class": "paragraph"}},
    "eltiempo": {"html_tag": "div", "indicator": {"class": "articulo-contenido"}}
}
url = "https://www.eltiempo.com/justicia/delitos/caso-mintic-envian-a-la-carcel-a-emilio-tapia-y-otros-dos-capturados-620526"
pagina = "eltiempo"
indicator = pages_indicator[pagina]

response = NewsScraper(url).get_news()
parser = ParserNews(response)
raw_text = parser.parse_page(indicator)
# save file to txt
with open("data/raw_article/"+pagina+"caso-mintic-envian-a-la-carcel.txt", "w", encoding="utf-8") as file:
    file.write(raw_text)
