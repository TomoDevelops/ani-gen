# https://animestore.docomo.ne.jp/animestore/rest/WS000107?start=20&length=20&mainKeyVisualSize=2&genreCd=11&_=1657514295581
# Results are loaded in a batch of 20
# start parameter shows where to start
# e.g. first 20 has no start param
#     21-40 is start=20
# length=20 is specifying 20 results per load but cannot seem to pass more than 20
# BELOW LOADS 300 ENTRIES START=300 (0 INDEXED)
# https://animestore.docomo.ne.jp/animestore/rest/WS000107?mainKeyVisualSize=2&genreCd=11&_=1657514295586
# genreCd=11 is the specifier that specifies the genre
# 11 = SF/fantasy, 12 = Robot/mech, 13 = Action/Battle etc.

import json
import requests
from bs4 import BeautifulSoup
from math import ceil
from get_genre import all_genre

# store the URL in url as
# parameter for urlopen
url_1 = "https://animestore.docomo.ne.jp/animestore/rest/WS000107?start="
url_2 = "&length=300&mainKeyVisualSize=2&"
url_3 = "&_=1657514295581"


# store the response of URL
for num in range(len(all_genre)):
    data = []
    for cnt in range(ceil(all_genre[num]['genre_cnt'] / 300)):
        response = requests.get(f"{url_1}{cnt * 300}{url_2}{all_genre[num]['genre_id']}{url_3}")
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        new_data = response.json()['data']['workList']
        for item in new_data:
            desc_response = requests.get(url=item['workInfo']['link']).text
            desc_content = BeautifulSoup(desc_response, "html.parser").select('.outlineContainer p')
            new_entry = {
                "title": item['workInfo']['workTitle'],
                "link": item['workInfo']['link'],
                "img_link": item['workInfo']['mainKeyVisualPath'],
                "desc": str
            }
            for desc in desc_content:
                desc_text = desc.text.strip()
                new_entry['desc'] = desc_text
            data.append(new_entry)
    with open(f"./data/{all_genre[num]['title'].replace('/','')}.json", 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print(f"Completed: {all_genre[num]['title'].replace('/','')}.json")
