import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class JohnLewisScraper(scrapy.Spider):
    name = "johnlewis_scraper"

    start_urls = [
        "https://www.johnlewis.com/browse/women/womens-boots/_/N-7oo3"
    ]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pipelines.JsonPipeline": 300,
        },
        "LOG_ENABLED": False,
    }

    def parse(self, response):
        # Parse the response data using XPath selectors

        # follow links and scrape data from other pages

        for link in response.css("a::attr(href)").getall():
            if link is not None and "/p" in link:
                yield response.follow(link, callback=self.parse_page)

    def parse_page(self, response):
        # Parse individual page data

        url = response.url

        description = self.get_product_description(response)

        
        try:
            specs_data = self.get_product_specification(response)

            data = {"prompt": specs_data, "completion": description, "url": url}

            yield data

        except Exception as e:
            print("Error in scraping data ", e)


    def get_product_description(self, response):
        """Get the product description from the product page"""

        all_description = response.xpath(
            '//*[@data-cy="product-description"]/div/p'
        ).extract()

        all_description_text = []

        for i in range(len(all_description)):

            description = response.xpath(
                f'//*[@data-cy="product-description"]/div/p[{i+1}]/text()'
            ).get()

            if description:
                all_description_text.append(description)

        description = "\n".join(all_description_text)

        return description



        description = response.xpath(
            '//*[@data-cy="product-description"]/div/p[1]/text()'
        ).get()

        return description

    def get_product_specification(self, response):
        """Get the product specification from the product page"""

        specs_count = response.xpath(
            f'//*[@data-cy="product-specification"]/ul/li'
        ).extract()

        all_spec_text = []

        for i in range(len(specs_count)):
            specification_key = response.xpath(
                f'//*[@data-cy="product-specification"]/ul/li[{i+1}]/strong/text()'
            ).get()

            specification_value = response.xpath(
                f'//*[@data-cy="product-specification"]/ul/li[{i+1}]/p/text()'
            ).get()

            if specification_key and specification_value:
                all_spec_text.append(f"{specification_key} is {specification_value}.")

        all_spec_text = " ".join(all_spec_text)

        return all_spec_text


# Run the scraper

process = CrawlerProcess(settings=get_project_settings())


process.crawl(JohnLewisScraper)
process.start()
