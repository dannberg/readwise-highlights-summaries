import requests
import smtplib
import configparser
from email.message import EmailMessage
from datetime import datetime


# Read credentials from a configuration file
config = configparser.ConfigParser()
config.read('config.ini')

READWISE_API_KEY = config.get('Readwise', 'API_KEY')
GPT_API_KEY = config.get('Chat-GPT', 'API_KEY')
EMAIL_ADDRESS = config.get('Email', 'ADDRESS')
EMAIL_PASSWORD = config.get('Email', 'PASSWORD')
RECIPIENT_EMAIL = config.get('Email', 'TO_ADDRESS')
SMTP_SERVER = config.get('Email', 'SMTP_SERVER')


def fetch_highlights():
    url = "https://readwise.io/api/v2/highlights/"
    headers = {"Authorization": f"Token {READWISE_API_KEY}"}
    params = {"page_size": 10, "order": "-updated"}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        # print(f"Response status code: {response.status_code}")
        # print(f"Response content: {response.content}")
        return None

    highlights_data = response.json()["results"]
    return highlights_data

def summarize_highlights(highlights_data):
    url = 'https://api.openai.com/v1/engines/text-davinci-002/completions'
    headers = {
        'Authorization': f'Bearer {GPT_API_KEY}',
        'Content-Type': 'application/json'
    }
    summaries_data = []

    for highlight in highlights_data:
        prompt = f"The following is an excerpt from a news article. It has been highlighted because it represents a key point from the article. Compose a tweet espousing the key point that this excerpt is making: \"{highlight['text']}\""
        data = {'prompt': prompt, 'max_tokens': 280}

        response = requests.post(url, headers=headers, json=data)
        summary = response.json()['choices'][0]['text'].strip().replace('\n', ' ')
        source_url = highlight.get('source_url', highlight['url'])
        summaries_data.append({
            'highlight': highlight['text'],
            'summary': summary,
            'url': source_url
        })

    return summaries_data

def send_email(highlights_and_summaries_data):
    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        # server.set_debuglevel(1)  # Enable debugging output
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = EmailMessage()
        msg['Subject'] = f'Your Tweet Summaries for {datetime.now().strftime("%B %d, %Y")}'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL

        formatted_highlights_and_summaries = []
        for i, data in enumerate(highlights_and_summaries_data):
            formatted_highlights_and_summaries.append(
                f"Highlight {i + 1}\n"
                f"Highlight: \"{data['highlight']}\"\n"
                f"Summary: \"{data['summary']}\"\n"
                f"Link: {data['url']}\n\n"
            )

        plain_content = "\n".join(formatted_highlights_and_summaries)
        msg.set_content(plain_content)

        # print("Email content:\n")
        # print(plain_content)
        server.send_message(msg)


highlights_data = fetch_highlights()
summaries_data = summarize_highlights(highlights_data)
send_email(summaries_data)
