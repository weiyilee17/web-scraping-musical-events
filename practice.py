from requests import get
from selectorlib import Extractor
from pandas import read_csv
from time import sleep, localtime, strftime, strptime, time
from streamlit import plotly_chart
from plotly.express import line


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
    with open('temperatures.txt', 'a') as file:
        file.write(f'{current_time},{temp}\n')


def get_structured_time(formatted_date):
    return strptime(formatted_date, '%y-%m-%d-%H-%M-%S')


if __name__ == '__main__':
    for i in range(5):
        extracted_temp = extract(scrape(URL))

        now = time()
        structured_current_time = localtime(now)
        formatted_time = strftime('%y-%m-%d-%H-%M-%S', structured_current_time)

        store_temperature(formatted_time, extracted_temp)

        sleep(2)

    data_frame = read_csv('temperatures.txt', parse_dates=['date'], date_parser=get_structured_time)

    x_axis = [strftime('%H:%M:%S', single_date) for single_date in data_frame['date']]
    y_axis = [int(single_temp) for single_temp in data_frame['temperature']]

    figure = line(
        data_frame=data_frame,
        x=x_axis,
        y=y_axis,
        labels={
            'x': 'Date',
            'y': 'Temperature (C)'
        }
    )

    plotly_chart(figure)