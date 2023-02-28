from requests import get
from time import sleep
from selectorlib import Extractor
from sqlite3 import connect

from send_email import send_email

URL = 'https://programmer100.pythonanywhere.com/tours/'


def scrape(url):
    """Scrape the page source from the URL"""
    response = get(url)
    html_source_code = response.text

    return html_source_code


def extract(html_code):
    extractor = Extractor.from_yaml_file('extract.yaml')
    extracted_value = extractor.extract(html_code)['tours']

    return extracted_value


def store_musical_events(musical_event):
    connection = connect('database.db')

    band, city, date = musical_event.split(', ')

    cursor = connection.cursor()
    cursor.execute('INSERT INTO events VALUES (?, ?, ?)', [band, city, date])
    connection.commit()

    connection.close()


def get_musical_events(scraped_info):
    connection = connect('database.db')

    band, city, date = scraped_info.split(', ')

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM events WHERE band=? AND city=? and date=?', (band, city, date))
    target_row = cursor.fetchall()

    connection.close()

    return target_row


if __name__ == '__main__':
    while True:
        extracted_info = extract(scrape(URL))
        print(extracted_info)

        if extracted_info != 'No upcoming tours':
            if not get_musical_events(extracted_info):
                store_musical_events(extracted_info)

                event_name, event_location, event_time = extracted_info.split(', ')
                send_email(
                    subject='New musical event was found!',
                    message=f'The event {event_name} would be hosted in {event_location}, on {event_time}'
                )
        sleep(2)
