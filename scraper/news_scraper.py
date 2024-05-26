# import requests
# from parsel import Selector
#
#
# class NewsScraper:
#     URL = "https://www.gazeta.ru/tech/news/2024/05/21/23060833.shtml"
#     HEADERS = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#         "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
#         "User-Agent":
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
#     }
#     PHONE_NUMBER = '//span[@itemprop="telephone"]/text()'
#     DESCRIPTION_XPATH = '//h1[@class="subheader"]/text()'
#     DATE_XPATH = '//div[@class="time"]'
#     IMAGE_XPATH = '//div[@class="zoombtn"]'
#     TITLE_XPATH = '//h2[@class="headline"]/text()'
#     LINK_XPATH = '//div[@class="b_article-text"]/p/a/@href'
#
#     def scrape_data(self):
#         response = requests.get(self.URL, headers=self.HEADERS)
#         # print(response.text)
#         tree = Selector(text=response.text)
#         imgs = tree.xpath(self.IMAGE_XPATH).getall()
#         titles = tree.xpath(self.TITLE_XPATH).getall()
#         dates = tree.xpath(self.DATE_XPATH).getall()
#         descriptions = tree.xpath(self.DESCRIPTION_XPATH).getall()
#         links = tree.xpath(self.LINK_XPATH).getall()
#         print(links)
#         return links[:5]
#         # for description in descriptions:
#         #     print(description)
#
#     async def scrape_data(self):
#         response = requests.get(self.URL, headers=self.HEADERS)
#         tree = Selector(text=response.text)
#         news_links = tree.xpath(self.NEWS_XPATH).getall()
#         return news_links[:5]
#
#     async def save_to_database(self, news_data):
#         conn = await db_connect()
#         async with conn.transaction():
#             for link in news_data:
#                 await conn.execute(
#                     INSERT_NEWS_QUERY,
#                     link
#                 )
#
#
# if __name__ == "__main__":
#     scraper = NewsScraper()
#     scraper.scrape_data()



