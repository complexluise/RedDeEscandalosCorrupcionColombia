import requests
import logging
from bs4 import BeautifulSoup


# Create logger
LOG = logging.getLogger("get txt from any news")
logging.basicConfig(level=logging.INFO)


class NewsScraper:
    def __init__(self, url: str):
        self.url = url

    def get_news(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            LOG.info(f"Successfully fetched page: {self.url}")
            return response.content
        else:
            LOG.error(
                f"Error fetching page: {self.url} - status code: {response.status_code}"
            )
            raise Exception(
                f"Error fetching page: {self.url} - status code: {response.status_code}"
            )


class ParserNews:
    def __init__(self, html_content: str):
        self.html_content = html_content
        self.soup = BeautifulSoup(self.html_content, "html.parser")

    def parse_page(self, indicator: dict) -> str:
        """Parse the page content and extract the text from the specified div element."""

        html_tag = indicator["html_tag"]

        if indicator.get("indicator"):
            html_indicator = indicator["indicator"]
            div_element = self.soup.find(html_tag, html_indicator)
        else:
            div_element = self.soup.find(html_tag)
        return div_element.get_text(strip=True, separator=" ")


if __name__ == "__main__":
    row = {
        "Link": "https://www.elcolombiano.com/colombia/politica/contraloria-entrego-informe-de-contratos-de-centros-poblados-con-mintic-DB14952895",
        "Nombre Entidad": "elcolombiano",
        "Escandalo": "Centros Poblados",
    }

    url = row["Link"]
    pagina = row["Nombre Entidad"]
    escandalo = row["Escandalo"]
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
    try:
        response = NewsScraper(url).get_news()  # TODO Iniciar fuera del for
        parser = ParserNews(response)
        raw_text = parser.parse_page(indicator)
        # save file to txt
        with open(
            "data/raw_article/" + pagina + filename + ".txt", "w", encoding="utf-8"
        ) as file:
            LOG.info("Saving file: %s", filename)
            file.write(raw_text)
    except Exception as e:
        LOG.error("Error processing row: %s", filename)
        LOG.error(e)
