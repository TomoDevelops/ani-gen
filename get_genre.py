from bs4 import BeautifulSoup
import requests

D_ANIME_URL = "https://animestore.docomo.ne.jp/animestore/"
D_ANIME_GENRE_URL = "gen_sel_pc"
all_genre = [
    # {
    #     "genre_id": str,
    #     "title": str,
    #     "url": str,
    #     "genre_cnt": int
    # }
]

response = requests.get(url=f"{D_ANIME_URL}{D_ANIME_GENRE_URL}")
text = response.text
soup = BeautifulSoup(text, "html.parser")
genre_html = soup.select("li.btnList a")
genre_title = [item.text.split('(')[0].strip() for item in genre_html]
genre_cnt = [int(item.text[item.text.find("(")+1:item.text.find(")")]) for item in genre_html]
genre_url = [item.get("href") for item in genre_html]
genre_id = [item.split('?')[-1] for item in genre_url]


for title, cnt, url, genre_id in zip(genre_title, genre_cnt, genre_url, genre_id):
    genre = {
        "genre_id": genre_id,
        "title": title,
        "url": url,
        "genre_cnt": cnt
    }
    all_genre.append(genre)