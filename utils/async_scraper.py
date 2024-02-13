from utils.config import URL_TEMPLATE, logger

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL Template: https://auto.ria.com/uk/car/used/?page={}

scraped_urls = {}


def get_number_of_pages(url: str) -> int:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    element = soup.find("span", class_="page-item dhide text-c")
    number_of_pages = element.text.replace(" ", "").split("/")[-1]

    return int(number_of_pages)


async def get_urls_from_page(page_number, session):
    urls = []
    url = URL_TEMPLATE.format(page_number)

    async with session.get(url) as resp:
        page = await resp.text()
        soup = BeautifulSoup(page, 'html.parser')
        elements = soup.find_all("a", class_="m-link-ticket")

        for e in elements:
            urls.append(e['href'])

        scraped_urls[page_number] = urls


async def get_all_urls(number_of_pages):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for page_number in range(1, number_of_pages+1):
            task = asyncio.create_task(get_urls_from_page(page_number, session))
            tasks.append(task)
            if len(tasks) == 30 or len(tasks) > 0:  # 10
                await asyncio.gather(*tasks)
                tasks = []

    await asyncio.sleep(5)

    return scraped_urls


def get_username(soup):
    username = soup.find("div", class_="seller_info_name bold")
    if username is None:
        username = soup.find("h4", class_="seller_info_name")
    if username is None:
        username = soup.find("h4", class_="seller_info_name grey bold")
    if username is None:
        return ""

    return username.text.strip().replace('"', "").replace("'", "`")


def get_phone_number(auto_id, json):
    userSecureHash = json["userSecure"]["hash"]
    url2 = f"https://auto.ria.com/users/phones/{auto_id}?hash={userSecureHash}"
    phone = requests.get(url2).json()
    phone = phone["phones"][0]["phoneFormatted"]
    phone = phone.replace(")", "").replace("(", "").replace(" ", "")
    phone = int("38" + phone)

    return phone


def get_car_number(soup):
    car_number = soup.find("span", class_="state-num ua")
    if car_number is None:
        return ""

    return car_number.text.split(" М")[0]


def get_car_vin(soup):
    car_vin = soup.find("span", class_="label-vin")
    if car_vin is None:
        car_vin = soup.find("span", class_="vin-code")
    if car_vin is None:
        return ""

    return car_vin.text.strip()


async def get_data_from_url(url, session):
    async with session.get(url) as resp:
        page = await resp.text()
        soup = BeautifulSoup(page, 'html.parser')

        if soup.find("div", class_="notice_head") is not None:
            return None

        auto_id = url.split('_')[-1][:-5]
        json_url = f"https://auto.ria.com/demo/bu/mainPage/rotator/item/{auto_id}"
        json = requests.get(json_url).json()

        url = url
        title = soup.find("h1", class_="head").text.strip()
        price_usd = int(json["USD"].replace(' ', ''))
        odometer = int(soup.find("span", class_="size18").text.strip())*1000
        username = get_username(soup)
        phone_number = get_phone_number(auto_id, json)
        image_url = json["photoBig"]
        images_count = int(soup.find("span", class_="count").find("span", class_="mhide").text.split()[-1])
        car_number = get_car_number(soup)
        car_vin = get_car_vin(soup)
        datetime_found = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin, datetime_found)
