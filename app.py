import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from data_collection.inference_product_scraper import scrape_this_johnlewis_url

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        user_text = request.form["user_text"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(user_text),
            temperature=0,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/finetuning", methods=("GET", "POST"))
def finetune_index():
    if request.method == "POST":
        try:
            user_text = request.form["user_text"]
            prompt = scrape_this_johnlewis_url(user_text)
            response = openai.Completion.create(
                model="ada:ft-personal:johnlewis-products-2023-05-19-16-06-01",
                prompt=prompt,
                temperature=0.6,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["END"],
            )
            return redirect(
                url_for(
                    "finetune_index", result=response.choices[0].text, prompt=prompt
                )
            )
        except Exception as e:
            print("Error in inferencing", e)
            return redirect(
                url_for(
                    "finetune_index", result="Error in inference", prompt=f"Error {e}"
                )
            )

    result = request.args.get("result")
    prompt = request.args.get("prompt")
    return render_template("finetune_index.html", result=result, prompt=prompt)


def generate_prompt(user_text):
    return f"Correct this to standard English:\n\n${user_text}."


def generate_prompt_for_finetuned(user_text):
    processed_prompt = ""
    for text_lines in user_text.split("\n")[1:]:
        specification_key = text_lines.split(":")[0].strip()
        specification_value = text_lines.split(":")[1].strip()
        if specification_key and specification_value:
            processed_prompt += f"{specification_key} is {specification_value}."

    return processed_prompt
