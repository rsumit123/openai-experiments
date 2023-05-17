import json


class JsonPipeline:
    """Custom Pipeline to save the scraped data to a JSON file"""

    def __init__(self):
        self.items = []

    def open_spider(self, spider):
        """Called when the spider is opened."""
        pass

    def close_spider(self, spider):
        """Called when the spider is closed. It saves the collected items to the JSON file."""

        print(f"Total items collected => {len(self.items)}")

        with open("product_data.json", "w") as file:
            json.dump(self.items, file)

    def process_item(self, item, spider):
        """Called for each yielded item. It appends the item to the self.items list."""

        if item["prompt"] and item["completion"]:
            if len(item["prompt"]) > 5 and len(item["completion"]) > 5:
                self.items.append(item)
        return item
