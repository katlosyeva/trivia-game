import requests


def get_questions_from_api(url):
    response = requests.get(url)
    return response.json()
