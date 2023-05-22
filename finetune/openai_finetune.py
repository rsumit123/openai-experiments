import pandas as pd
import openai
import subprocess
import sys
import time
import os


openai_api_key = os.getenv("OPENAI_API_KEY")

try:
    if sys.argv[1] == "prepare" or sys.argv[1] == "all":
        print("Preparing data....")
        # Read the data
        if sys.argv[2] == "training":
            print("reading training data")
            filename = "data_collection/data/product_data.csv"

        else:
            print("No second argument found. Reading validation data")
            filename = "data_collection/data/validation_data.csv"

        df = pd.read_csv(filename)

        prepared_data = df.drop("url", axis=1)

        prepared_data.to_csv(filename.split(".")[0] + "_prepared.csv", index=False)

        ## prepared_data.csv --> prepared_data_prepared.json
        subprocess.run(
            f'openai tools fine_tunes.prepare_data --file {filename.split(".")[0]+"_prepared.csv"} --quiet'.split()
        )
    if sys.argv[1] == "train" or sys.argv[1] == "all":
        print("Training.... This will consume your OpenAI credits.")
        print("Press Ctrl + C to stop...")
        time.sleep(5)
        ## Start fine-tuning

        subprocess.run(
            'openai api fine_tunes.create --training_file data_collection/data/product_data_prepared_prepared.jsonl -v data_collection/data/validation_data_prepared_prepared.jsonl --model ada --suffix "johnlewis_products"'.split(),
            env=dict(OPENAI_API_KEY=openai_api_key, **os.environ),
        )

except IndexError as e:
    print(
        "One or more, command line arguments maybe missing. Please provide all the arguments. Example: python openai_finetune.py prepare training"
    )

except Exception as e:
    print("Error in finetuning", e)
