import requests
from bs4 import BeautifulSoup

# Пробігаюсь по 20 сторінкам сайту(в кожній по 50 фільмів)
for i in range(1,21):
    #Створюю змінну з посиланням на сайт
    url = f"https://ru.kinorium.com/collections/critics/131/?order=sequence&page={i}&perpage=50&show_viewed=1"
    # Роблю get запрос
    req = requests.get(url).text
    # Перетворюю на читабельний html код
    First_block_soup = BeautifulSoup(req, "lxml")
    # Пробігаюсь за допомогою циклу по кожному фільму
    for film_num in range(0,51):
        # Отримую посилання на окремий фільм
        films_url = First_block_soup.find_all("div", class_="filmList__item-wrap-title")[film_num].find("a").get("href")
        # Роблю запит
        film_url_req = requests.get("https://ru.kinorium.com" + films_url).text
        # Суп
        film_web_soup = BeautifulSoup(film_url_req, "lxml")
        
        # Отримую всю мені необхідну інформацію
        film_name = film_web_soup.find("h1", class_ = "film-page__title-text film-page__itemprop").text
        film_year = film_web_soup.find("span", class_ = "film-page__title-label").text
        film_description = film_web_soup.find("section", itemprop="description").text.replace("Описание", "")
        film_country = film_web_soup.find("a", class_ = "film-page__country-link").text
        
        # Записую інформацію про фільм у текстовий документ
        with open("films.txt", "w") as f:
            result = f"""{film_num}. {film_name}
            Год: {film_year}
            Страна: {film_country}
            {film_description}
            """
            f.write(result)
        # На жаль не вдалося завершити проект так як я хотів, адже через велику кількість запитів
        # сайт мене заблокував. Треба було бути більш рацональним та зберегти сайт окремо.
