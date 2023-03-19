# Readwise Highlights Summary

This Python script fetches your latest highlights from Readwise, generates snarky, humorous tweet summaries using OpenAI's GPT-3, and emails the results to you.

I created this because I'm so bad at remembering to post on Mastodon, and I figured that regular reminders to post, along with examples of possible content, might help me share more.

## Prerequisites

1. Python 3.6 or higher
2. A [Readwise](https://readwise.io/) account with an API key
3. An [OpenAI](https://platform.openai.com/) account with an API key
4. An email account with SMTP access

## Installation

1. Clone the repository or download the `readwise_highlights_summary.py` file.

2. Install required packages:

```bash
pip install -r requirements.txt
```


3. Create a `config.ini` file in the same directory as the script. Add your Readwise API key, OpenAI API key, and email credentials:

```
[Readwise]
API_KEY = your_readwise_api_key

[Chat-GPT]
API_KEY = your_openai_api_key

[Email]
SMTP_SERVER = your_smtp_server
ADDRESS = your_email_address
PASSWORD = your_email_password
TO_ADRESS = your_to_email_address
```



## Usage

Run the script:

```
python readwise_highlights_summary.py
```


You will receive an email with your latest highlights and generated tweet summaries.

## Note

This script is intended for educational purposes only. Please ensure you comply with the terms of service of the respective APIs.

This code was written with assistance from OpenAI's [GPT-4](https://openai.com/product/gpt-4).
