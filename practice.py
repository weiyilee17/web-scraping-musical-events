from requests import get
from selectorlib import Extractor
from time import sleep, localtime, strftime, time
from sqlite3 import connect


URL = 'https://programmer100.pythonanywhere.com/'


def scrape(url):
    response = get(url)
    html_source_code = response.text

    return html_source_code


def extract(html_code):
    extractor = Extractor.from_yaml_file('temperature_extract.yaml')
    extracted_value = extractor.extract(html_code)['temp']

    return extracted_value


def store_temperature(current_time, temp):
    connection = connect('database.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO temperatures VALUES (?, ?)', [current_time, int(temp)])
    connection.commit()

    connection.close()


if __name__ == '__main__':
    for i in range(5):
        extracted_temp = extract(scrape(URL))

        now = time()
        structured_current_time = localtime(now)
        formatted_time = strftime('%y-%m-%d-%H-%M-%S', structured_current_time)

        store_temperature(formatted_time, extracted_temp)

        sleep(2)
