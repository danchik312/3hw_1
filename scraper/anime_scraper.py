import requests
from parsel import Selector

class AnimeScraper:
    URL = "https://animestars.org/"
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }
    PHONE_NUMBER = '//div[@class="footer-num "]/a/text()'
    DESCRIPTION_XPATH = '//p[@class="remove-outline"]/text()'
    DATE_XPATH = '//div[@class="col-sm-8 col-lg-9 pull-left card"]/h3/small/text()'
    IMAGE_XPATH = '//div[@class="row newsCards"]//img/@src'
    TITLE_XPATH = '//div[@class="col-sm-8 col-lg-9 pull-left card"]/h3/text()'
    LINK_XPATH = '//img[@class="lazy-loaded"]/@data-src'

    def scrape_data(self):
        response = requests.get(self.URL, headers=self.HEADERS)
        # print(response.text)
        tree = Selector(text=response.text)
        imgs = tree.xpath(self.IMAGE_XPATH).getall()
        titles = tree.xpath(self.TITLE_XPATH).getall()
        dates = tree.xpath(self.DATE_XPATH).getall()
        descriptions = tree.xpath(self.DESCRIPTION_XPATH).getall()
        links = tree.xpath(self.LINK_XPATH).getall()
        print(links)
        return links[:5]

    async def get_pages(self, limit=300):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            get_page_tasks = [self.fetch_page(client, page) for page in range(1, limit + 1)]
            pages = await asyncio.gather(*get_page_tasks)

            scraping_tasks = [self.scrape_data(selector) for selector in pages if pages is not None]
            await asyncio.gather(*scraping_tasks)

    async def fetch_page(self, client, page):
        url = self.URL.format(page=page)
        response = await client.get(url, timeout=20.0)
        print("page: ", page)
        return Selector(response.text)

    async def scrape_dat(self, selector):
        links = selector.xpath(self.LINK_XPATH).getall()
        print(links)


if __name__ == "__main__":
    scraper = AnimeScraper()
    scraper.scrape_data()
    asyncio.run(scraper.get_pages())