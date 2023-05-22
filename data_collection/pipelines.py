import json
import Levenshtein
import pandas as pd


class JsonPipeline:
    """Custom Pipeline to save the scraped data to a JSON file"""

   



    def __init__(self, mode="validation"):
        self.items = []
        self.mode = mode
        if self.mode == "validation":
            with open("data/product_data.json", "r") as file:
                self.training_items = json.load(file)

    def open_spider(self, spider):
        """Called when the spider is opened."""
        pass

    def close_spider(self, spider):
        """Called when the spider is closed. It saves the collected items to the JSON file."""
        filename = "data/product_data" if self.mode == "training" else "data/validation_data"

        processed_items = []

        if self.mode == "validation":

            for current_item in self.items:
                for training_item in self.training_items:
                    if (
                       current_item["url"] == training_item["url"]
                    ):
                        break
                else:
                    processed_items.append(current_item)

        else:
            processed_items = self.items



        print(f"Total items collected => {len(processed_items)}")

        with open(f"{filename}.json", "w") as file:
            json.dump(processed_items, file)

        self.convert_to_csv(filename, processed_items)

    def process_item(self, item, spider):
        """Called for each yielded item. It appends the item to the self.items list."""

        # item = self.add_separators(item)

        if item["prompt"] and item["completion"]:
            if len(item["prompt"]) > 5 and len(item["completion"]) > 5:
                if len(self.items) == 0:
                    
                    self.items.append(item)
                for e_item in self.items:
                    if (
                        Levenshtein.ratio(e_item["completion"], item["completion"])
                        > 0.8
                    ):
                        break
                else:
                    
                    self.items.append(item)

        return item

    def add_separators(self, item):
        """Add some separators to the prompt and completion according to OPENAI's guidelines"""

        item["prompt"] = item["prompt"] + "\n\n###\n\n"
        item["completion"] = item["completion"] + "###\n\n"

        return item
    
    def convert_to_csv(self, filename, processed_items):
        """Convert list of items to csv file"""
            
        df = pd.DataFrame(processed_items)
        df.to_csv(f"{filename}.csv", index=False)
