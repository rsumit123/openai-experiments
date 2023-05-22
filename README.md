# OpenAI Experiments

This app uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. Check out the tutorial or follow the instructions below to get set up.

## Steps taken to finetune the model

### Data Preparation

For preparing the data, johnlewis (https://johnlewis.com) website was scraped for categories womens-shoes, womens-boots, mens-trainers and mens-shoes. Product specification and Product description was scraped from the product pages of mentioned categories. Both product specification data and description were transformed in a manner so that the model would be able to understand clearly, as the number of training samples used was limited (320 training samples). Levenshtein distance was used to separate similar looking datapoints as they would not present any extra information in training.


### Model Selection 

OpenAI's model "Ada" (GPT-3 series) was chosen for this task as this model had the lowest cost among all. Better models like the davinci or the GPT-3.5 series can also be chosen for better results.


### Finetuning

Data was prepared as per the expected input of the model, in pairs of prompts and completion, where prompts are the specification of the product (transformed) and completions are the expected description. After that, a finetuning job was queued using OpenAI's CLI. A validation set of 50 samples was also provided with 320 training samples. The model took about 15 minutes of time to finetune for 4 epochs, after which it was ready for inference. For inference, the parameters being used are temperature = 0.6, top_p = 1, frequency_penalty = 0, presence_penalty = 0, max_tokens = 256. These values were decided upon through experimentation and some common knowledge. Currently, the model can be inferenced on https://openai-experiments.onrender.com/finetuning.

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd openai-experiments
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

8. Run the app:

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)!.
