from time import strftime, strptime
from streamlit import plotly_chart
from plotly.express import line
from sqlite3 import connect


def get_temp():
    connection = connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT temperature FROM temperatures')

    all_temperatures = cursor.fetchall()

    connection.close()

    return all_temperatures


def get_date():
    connection = connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT date FROM temperatures')

    all_dates = cursor.fetchall()

    connection.close()

    return all_dates


def get_structured_time(formatted_date):
    return strptime(formatted_date, '%y-%m-%d-%H-%M-%S')


# Initially tried to SELECT all and destructured to x and y-axis, thus only 1 query is made, but for the sake of
# practice and remind not to select all on anything, wrote 2 functions for it.
x_axis = [strftime('%H:%M:%S', get_structured_time(date)) for (date,) in get_date()]
y_axis = [single_temperature for (single_temperature,) in get_temp()]

figure = line(
    x=x_axis,
    y=y_axis,
    labels={
        'x': 'Date',
        'y': 'Temperature (C)'
    }
)

plotly_chart(figure)
