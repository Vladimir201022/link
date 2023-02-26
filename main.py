import os
import argparse
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse
from requests.exceptions import HTTPError


def shorten_link(token, url):
    bitly_url = "https://api-ssl.bitly.com/v4/shorten"
    params = {"long_url": url}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(bitly_url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(token, bitlink):
    bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    params = {"unit": "month", "units": "-1"}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(bitly_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(token, url):
    bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(bitly_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    web_token = os.getenv['BITLY_TOKEN']
    parser = argparse.ArgumentParser(
        description=
        'Эта программа позволяет посчитать клики по ссылкам и сократить ссылку. Для того, чтобы получить колличество кликов введите --url'
    )
    parser.add_argument('--url', type=str, help='Введите ссылку: ')
    args = parser.parse_args()
    parse_url = urlparse(args.url)
    url_without_protocol = f"{parse_url.netloc}{parse_url.path}"

    if is_bitlink(web_token, url_without_protocol):
        try:
            print(count_clicks(web_token, url_without_protocol))
        except HTTPError as error:
            exit(f"Ошибка при подсчете кликов{error}")
    else:
        try:
            print(shorten_link(web_token, args.url))
        except HTTPError as error:
            exit(f"Проверьте ссылку,ошибка{error}")


if __name__ == "__main__":
    main()
