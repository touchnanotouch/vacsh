from src.scraping.HHScraper import HHScraper


if __name__ == "__main__":
    scraper = HHScraper(query="Python+Junior", max_pages=1)
    vacancies = scraper.scrape()
    scraper.save_to_csv("data/vacancies.csv")

    print(f"Сохранено {len(vacancies)} вакансий в data/vacancies.csv")
