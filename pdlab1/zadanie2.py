import requests
from bs4 import BeautifulSoup

# URL для получения данных о погоде

url = "https://www.gismeteo.ru/diary/4976/2023/9/"

try:
    # Отправляем GET-запрос к странице
    response = requests.get(url)
    response.raise_for_status()  # Проверяем, что запрос успешен

    # Парсим HTML-страницу с помощью BeautifulSoup и lxml парсера
    soup = BeautifulSoup(response.text, 'lxml')

    # Находим таблицу с данными о погоде
    table = soup.find("table", class_="w-archive")

    # Создаем CSV-файл для сохранения данных
    with open("dataset.csv", "w", newline="") as csv_file:
        for row in table.find_all("tr")[1:]:
            columns = row.find_all("td")
            date = columns[0].text.strip()
            temperature = columns[1].text.strip()
            pressure = columns[2].text.strip()
            wind = columns[3].text.strip()

            # Записываем данные в CSV-файл
            csv_file.write(f"{date},{temperature},{pressure},{wind}\n")

    print("Данные успешно сохранены в файл dataset.csv")

except requests.exceptions.RequestException as e:
    # Обработка ошибок запроса (например, отсутствие сети или недоступность сервера)
    print(f"Ошибка при выполнении запроса: {e}")
except Exception as e:
    # Обработка других ошибок
    print(f"Произошла ошибка: {e}")
