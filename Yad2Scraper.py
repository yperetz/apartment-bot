import time
from random import uniform
from bs4 import BeautifulSoup
import pickle
import re
import requests

headers_places = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'mainsite_version_commit': '3376126e2fad3570e3a7cd8102badd16e5644759',
    'mobile-app': 'false',
    'bouncerGuid': 'c1a5bc201e69b8fc9205c3bf07fbe01ed286016eedc66611cc598863c7382bfc',
    'bouncerTime': '1660263233753',
    'bouncerInst': 'true',
    'bouncerAccount': 'eyJYIjoiMjA0YWY3ZWRlOTZiMzk5YmRmMDkxOWFkZWU5ZDdjYzA1MzUyYjE2Zjg4ZWViY2RiNjlhZDQzNmY4ZjZiYzVmMSIsIlkiOiI1YmU0NWZiYmU5MjMxMjhkMGIwODY2NjkyMWEzNDI4ZGFmNGYwZTEyZjhlM2JmODQ1NWI0OWQ0NDVhNWMyMWExIn0=',
    'bouncerSignature': 'eyJyIjoiYjU5Y2JhYTcyOGMwOWFiMGMzOWI3OTA3NDVkY2IxNTFiMGMyZDI0ODA4YTA3ZDg5MzAxNGM3NDkzNjBkOTljNSIsInMiOiI2ZTg5NmVjMDQ2NmU5NjEwZWI4ZTI1MWEzN2Y4N2I1MWZiMDhjYzRhYWMwM2JjZjY0MmEzYTgzYTU5ZWUzY2E1In0=',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.yad2.co.il/realestate/rent',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '__uzma=ed4bb612-a4ba-4542-82ad-fc38a0d58292; __uzmb=1660263172; __uzme=2175; __uzmc=680841988958; __uzmd=1660263206; __uzmf=7f6000e24c32a7-8bda-40a7-a2d4-359ab0d0187c166026317248134452-82c8360fd311031c19; abTestKey=45; canary=never; __uzmhj=d8d6c4f1e2eb9503ccbf213e32c84039d04f89e5cdb8bf9a25638fd84fcdf711; __ssds=3; server_env=production; __ssuzjsr3=a9be0cd8e; __uzmaj3=812e8227-7889-4632-af90-75b7424a867a; __uzmbj3=1660263195; __uzmcj3=863611081734; __uzmdj3=1660263195; _ga_GQ385NHRG1=GS1.1.1660263199.1.1.1660263199.0; _ga=GA1.1.438239348.1660263199; y2018-2-cohort=64; leadSaleRentFree=99; y2_cohort_2020=33; use_elastic_search=1; favorites_userid=ghh405076372; bc.visitor_token=6963648583322460160',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

headers_aps = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '__uzma=ed4bb612-a4ba-4542-82ad-fc38a0d58292; __uzmb=1660263172; __uzme=2175; __uzmc=433928552165; __uzmd=1660265668; __uzmf=7f6000e24c32a7-8bda-40a7-a2d4-359ab0d0187c16602631724812496452-e494c31c9ed5ed6a85; abTestKey=45; canary=never; __uzmhj=d8d6c4f1e2eb9503ccbf213e32c84039d04f89e5cdb8bf9a25638fd84fcdf711; __ssds=3; server_env=production; __ssuzjsr3=a9be0cd8e; __uzmaj3=812e8227-7889-4632-af90-75b7424a867a; __uzmbj3=1660263195; __uzmcj3=909271399421; __uzmdj3=1660265668; _ga_GQ385NHRG1=GS1.1.1660265649.2.1.1660265666.0; _ga=GA1.1.438239348.1660263199; y2018-2-cohort=64; leadSaleRentFree=99; y2_cohort_2020=33; use_elastic_search=1; bc.visitor_token=6963648583322460160; recommendations-searched-2=2; recommendations-home-category={"categoryId":2,"subCategoryId":2}; _ga_10CMRFNKW7=GS1.1.1660265651.1.1.1660265666.0; favorites_userid=ghh405076372',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

URL_AUTOCOMPLETE = "https://www.yad2.co.il/api/search/autocomplete/realestate?text="
ROOMS_MIN = '1.5'
ROOMS_MAX = '2.5'
H_GID = 3
C_GID = 4
SLEEP = 2
SEP = "%"
PLACES = [{"city": "רמת גן", "hoods": ["רמת חן", "רמת השקמה"]},
          {"city": "תל אביב יפו", "hoods": ["ניר אביב"]}]


def sleep(sec=SLEEP, var=0.5):
    sec = sec + uniform(-var, var)
    time.sleep(sec)


# def encode_place(place):
#     encoded_place = place.encode("utf-8")
#     encoded_place = [hex(v)[2:] if len(hex(v)) > 3 else "0" + hex(v)[2:] for v
#                      in encoded_place]
#     encoded_place = SEP + SEP.join(encoded_place)
#     return encoded_place

def get_places(headers):
    """
    getting cities and neighborhoods info from autocomplete api
    :return: A list of dictionaries for each city. each element is the
    dictionary returned from the api with addition of the hoods key, which value
    is a list of dictionaries of relevant neighborhoods returned from the api
    """
    found_places = []
    for city_place in PLACES:
        city, hoods = city_place["city"], city_place["hoods"]
        city_found = {}
        r = requests.get(
            'https://www.yad2.co.il/api/search/autocomplete/realestate',
            params={'text': city}, headers=headers).json()
        for entry in r:
            if entry["groupID"] == C_GID:
                city_found = entry
                break

        sleep()

        hoods_found = []
        for h in hoods:
            r = requests.get(
                'https://www.yad2.co.il/api/search/autocomplete/realestate',
                params={'text': h + ', ' + city}, headers=headers).json()
            sleep()
            for entry in r:
                if entry["groupID"] == H_GID and entry["value"]["city"] == \
                        city_found["value"]["city"]:
                    hoods_found.append(entry)

        city_found["hoods"] = hoods_found
        found_places.append(city_found)
    return found_places


def get_apt_info(ft, ap_ids):
    item = ft.find('div', id=re.compile("^feed_item_\\d+$"))
    if item['item-id'] in ap_ids:
        return None
    ap_ids.append(item['item-id'])
    name_tag = ft.find('span', id=re.compile("^feed_item_\\d+_title$"))
    name = name_tag.text.strip()
    subttitle = name_tag.parent.find('span',
                                     class_='subtitle').text.strip()
    rooms = ft.find('span', id=re.compile("^data_rooms_\d+$")).text.strip()
    floor = ft.find('span', id=re.compile("^data_floor_\d+$")).text.strip()
    area = ft.find('span', id=re.compile("^data_SquareMeter_\d+$")).text.strip()
    img_url = ft.find('img', class_='feedImage')['src'].strip()
    img_re = re.search(r"(.+\.(jpe?g|png)).*", img_url)
    img_url = None
    if img_re is not None:
        if img_re.group(1) is not None:
            img_url = img_re.group(1)

    return {'name': name, 'id': item['item-id'], 'subtitle': subttitle,
            'rooms': rooms, 'floor': floor, 'area': area, 'img_url': img_url}


def get_all_apt_info(found_places, headers):
    rooms = ROOMS_MIN + '-' + ROOMS_MAX
    ap_ids = []
    all_aps = []
    for city in found_places:
        city_item = {'name': city['text'], 'id': city['value']['city'],
                     'nhoods': []}

        for nhood in city["hoods"]:
            # todo value
            nhood_item = {'name': nhood['text'],
                          'id': nhood['value']['neighborhood'],
                          'apartments': []}
            r = requests.get(
                'https://www.yad2.co.il/realestate/rent',
                params={'topArea': nhood['value']['topArea'],
                        'area': nhood['value']['area'],
                        'city': nhood['value']['city'],
                        'neighborhood': nhood['value']['neighborhood'],
                        'rooms': rooms, }, headers=headers)
            sleep()
            soup = BeautifulSoup(r.text, 'html.parser')
            feedtables = soup.findAll('div', class_='feeditem table')

            for ft in feedtables:
                aps = get_apt_info(ft, ap_ids)
                if aps is None:
                    continue
                nhood_item['apartments'].append(aps)
            city_item['nhoods'].append(nhood_item)
        all_aps.append(city_item)
    return all_aps


def get_aps():
    places = get_places(headers_places)
    return get_all_apt_info(places, headers_aps)
