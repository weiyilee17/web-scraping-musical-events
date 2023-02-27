from requests import get

from selectorlib import Extractor

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
    with open('musical_events.txt', 'a') as file:
        file.write(f'{musical_event}\n')


def get_musical_events():
    with open('musical_events.txt', 'r') as file:
        return file.read()


if __name__ == '__main__':
    extracted_info = extract(scrape(URL))
    print(extracted_info)

    if extracted_info != 'No upcoming tours':
        if extracted_info not in get_musical_events():
            store_musical_events(extracted_info)

            event_name, event_location, event_time = extracted_info.split(', ')
            send_email(
                subject='New musical event was found!',
                message=f'The event {event_name} would be hosted in {event_location}, on {event_time}'
            )
