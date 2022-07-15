from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import json
from random import choice, randint

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)

# App Functions

## Get Genre
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
genre_cnt = [int(item.text[item.text.find("(") + 1:item.text.find(")")]) for item in genre_html]
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


## Choose Anime
def choose_anime(genre, ranking):
    with open(f"./data/{genre}.json", 'r', encoding="utf-8") as file:
        data = json.load(file)
        if ranking > 0:
            return data[(randint(0, ranking))]
        else:
            return choice(data)


# Actual App
@app.route('/')
def home():
    return render_template('index.html', all_genre=all_genre)


@app.route('/results', methods=["POST"])
def results():
    if request.method == "POST":
        genre = request.form['genre']
        ranking = 0
        if bool(request.form['from_ranking']):
            ranking = int(request.form['ranking'])
        anime = choose_anime(genre, ranking)
        return render_template('results.html', anime=anime)
    return render_template('results.html')


if __name__ == "__main__":
    app.run(debug=True)
