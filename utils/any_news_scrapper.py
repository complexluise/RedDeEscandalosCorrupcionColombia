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
                f"Error fetching page: {self.url} - status code: {response.status_code}")
            raise Exception(
                f"Error fetching page: {self.url} - status code: {response.status_code}")


class ParserNews:

    def __init__(self, html_content: str):
        self.html_content = html_content
        self.soup = BeautifulSoup(self.html_content, "html.parser")

    def parse_page(self, indicator: dict) -> str:
        """Parse the page content and extract the text from the specified div element."""

        html_tag = indicator["html_tag"]
        html_indicator = indicator["indicator"]
        div_element = self.soup.find(html_tag, html_indicator)
        return div_element.get_text(strip=True, separator=" ")
