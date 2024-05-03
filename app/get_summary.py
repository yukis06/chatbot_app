from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import HumanMessage, SystemMessage


def get_content(url):
    """
    Fetches and returns the main content of a webpage given its URL.

    This function sends a GET request to the specified URL and attempts to parse the HTML content using BeautifulSoup.
    It prioritizes returning the text within the <main>, <article>, or <body> tags, in that order.

    Args:
        url (str): The URL of the webpage from which to fetch content.

    Returns:
        str: The main text content of the webpage. If an HTTP error occurs, it returns an error message.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request resulted in an unsuccessful status code.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.main:
            return soup.main.get_text()
        elif soup.article:
            return soup.article.get_text()
        else:
            return soup.body.get_text()
    except requests.exceptions.HTTPError as e:
        return f"Error fetching content from {url}: {e}"

def builed_promt(content: str, n_chars: int = 300):
    return f"""以下はとある。Webページのコンテンツである。内容を{n_chars}程度でわかりやすく要約してください。

    ========

    {content[:1000]}

    ========

    日本語で書いてね！
    """

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def ask_summary(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost 

def get_summary(url, llm):
    if not validate_url(url):
        return "Invalid URL. Please enter a valid URL."
    content = get_content(url)
    prompt = builed_promt(content)
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=prompt)
    ]
    response, cost = ask_summary(llm, messages)
    return response, cost