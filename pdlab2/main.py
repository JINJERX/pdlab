from bs4 import BeautifulSoup
import requests
import csv
import time
from retry import retry


@retry(exceptions=Exception, tries=3, delay=1, backoff=2)
def parse_td_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    time.sleep(1)
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    data = []

    for row in soup.select('tr[align="center"]'):
        date = row.select_one('td.first').text.strip()


        day_temp = row.select_one('td.first_in_group').text.strip()
        day_pressure = row.select_one('td.first_in_group').find_next('td').text.strip()
        day_wind = row.select_one('td > span').text.strip()



        data.append([date, day_temp, day_pressure, day_wind])

    return data


def save_to_csv(data, filename='output.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date', 'Temperature', 'Pressure', 'Wind'])
        csvwriter.writerows(data)


if __name__ == '__main__':
    url = 'https://www.gismeteo.ru/diary/4976/2023/9/'
    data = parse_td_content(url)
    if data:
        save_to_csv(data)
        print('сохранено в output.csv')
    else:
        print('Не удалось получить данные.')


