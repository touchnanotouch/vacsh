import re

import undetected_chromedriver as uc

from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class HHScraper:
    SEARCH_URL = "https://hh.ru/search/vacancy"

    def __init__(
        self,
        query: str = "Python+Junior",
        max_pages: int = 1,
        chrome_options: Optional[uc.ChromeOptions] = None,
    ):
        self.query = query
        self.max_pages = max_pages
        self.chrome_options = chrome_options or self._default_chrome_options()
        self.vacancies: List[Dict[str, str]] = []

    def _default_chrome_options(self) -> uc.ChromeOptions:
        options = uc.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        return options

    def scrape(self) -> List[Dict[str, str]]:
        self.vacancies.clear()

        for page in range(self.max_pages):
            url = (
                f"{self.SEARCH_URL}?text={self.query}"
                if page == 0
                else f"{self.SEARCH_URL}?text={self.query}&page={page}"
            )
            with uc.Chrome(options=self.chrome_options, headless=True) as driver:
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")
            cards = soup.find_all(
                "div",
                attrs={"data-qa": "vacancy-serp__vacancy"}
            )
            for card in cards:
                title_elem = card.find(
                    "span",
                    attrs={"data-qa": "serp-item__title-text"}
                )
                address_elem = card.find(
                    "span",
                    attrs={"data-qa": "vacancy-serp__vacancy-address"}
                )
                company_elem = card.find(
                    "span",
                    attrs={"data-qa": "vacancy-serp__vacancy-employer-text"}
                )
                experience_elem = card.find(
                    "span",
                    attrs={"data-qa": re.compile(r"vacancy-serp__vacancy-work-experience")}
                )
                link_elem = card.find(
                    "a",
                    attrs={"data-qa": "serp-item__title"}
                )
                self.vacancies.append(
                    {
                        "title": title_elem.text.strip() if title_elem else "Нет названия",
                        "address": address_elem.text.split()[0].strip() if address_elem else "Не указано",
                        "company": company_elem.text.strip() if company_elem else "Не указано",
                        "experience": experience_elem.text.strip() if experience_elem else "Не указано",
                        "link": link_elem["href"].split("?")[0].strip() if link_elem else "#",
                    }
                )

        return self.vacancies
