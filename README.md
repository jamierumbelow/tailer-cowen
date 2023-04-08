# tAIler cowen

!(https://github.com/jamierumbelow/tailer-cowen/blob/main/screenshot.png?raw=true)

TAIler Cowen is an AI that queries the Marginal Revolution blog and answers your questions based on the content found there.

## Prerequisites

- Python 3.7 or higher
- Virtualenv

## Setup

- Clone the repo
- Change into the tailer-cowen directory.
- Create a virtual environment and activate it:

  virtualenv venv
  source venv/bin/activate

- Install the required dependencies:

  pip install -r requirements.txt

- Copy the .env file and set your [OpenAI token](https://platform.openai.com/account/api-keys):

  cp .env.example .env

## Running TAIler Cowen

Run the main script.

- python main.py

When prompted, enter "y" to load from the cached embedding database or "n" to load from the sources

Loading sources will take a while (~7 minutes on my machine), but it will save the embeddings to the data/embeddings directory so that you can load them quickly in the future.

Enter your query, and TAIler Cowen will return a relevant answer based on the Marginal Revolution blog content.

## Embeddings

To help get started quickly, the embeddings are cached in the data/embeddings directory, as of 2023-04-08.

## Scrape sources

There is an additional script called scrape.py that can be used to scrape new content from the Marginal Revolution blog. Follow these steps to run the script:

- Make sure you are in the tailer-cowen directory and your virtual environment is activated.
- Run the scrape.py script:

  python scrape.py

This script will scrape new content from the Marginal Revolution blog and save it to the data directory, so that TAIler Cowen can use it to answer your queries.

Tyler and Alex write a _lot_, and the current scraper will trigger a `RecursionError` after ~1000 posts. The scraper will save the current page in data/marginal-revolution.json so you can run it again and it'll pick up where it last failed.
