from scrapy.http import HtmlResponse
from scrapy.http import Request
import requests
from .headers_cookies import headers, cookies


def get_product_specification(response):
    """Get the product specification from the product page"""

    specs_count = response.xpath(
        f'//*[@data-cy="product-specification"]/ul/li'
    ).extract()

    all_spec_text = []

    for i in range(1, len(specs_count)):
        specification_key = response.xpath(
            f'//*[@data-cy="product-specification"]/ul/li[{i+1}]/strong/text()'
        ).get()

        specification_value = response.xpath(
            f'//*[@data-cy="product-specification"]/ul/li[{i+1}]/p/text()'
        ).get()

        if specification_key and specification_value:
            all_spec_text.append(f"{specification_key} is {specification_value}.")

    all_spec_text = " ".join(all_spec_text)

    print(all_spec_text)

    return all_spec_text


def scrape_this_johnlewis_url(url):
    """make a request to the url and get the product specification"""

    if (
        url
        == "https://www.johnlewis.com/skechers-bobs-squad-chaos-face-off-trainers/p6377789"
    ):
        with open("data_collection/html_files/johnlewis.html", "r") as f:
            scrapy_response = HtmlResponse(url=url, body=f.read(), encoding="utf-8")
    else:
        print("making request....")
        response = requests.get(url, headers=headers)
        scrapy_response = HtmlResponse(url=url, body=response.text, encoding="utf-8")

    prod_specification = get_product_specification(scrapy_response)

    return prod_specification
