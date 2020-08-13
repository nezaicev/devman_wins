from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
import pandas
import argparse

from jinja2 import Environment, FileSystemLoader, select_autoescape

CREATION_DATE = datetime(year=1920, month=1, day=1)


def read_file_to_dict(path_file):
    products = pandas.read_excel(path_file, na_values=['N/A', 'NA'], keep_default_na=False)
    return products.to_dict(orient='records')


def validate_format_word(year):
    if int(str(year)[-1]) > 4 or str(year)[-1] == '0':
        return 'лет'
    elif str(year)[-1] == '1':
        return 'год'
    else:
        return 'года'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    parser = argparse.ArgumentParser(
        description='Формирует html страницу , запускает HTTP-сервер по адресу 127.0.0.1:8000'
    )
    parser.add_argument('path_to_file', help='Файл с информацией о товаре, формат xlsx')
    args = parser.parse_args()
    delta_year = CREATION_DATE.year - datetime.today().year
    products = read_file_to_dict(args.path_to_file)
    products_by_category = defaultdict(list)

    for i in products:
        products_by_category[i['Категория']].append(i)

    rendered_page = template.render(
        count_years=delta_year,
        word_year=validate_format_word(delta_year),
        products=products_by_category,

    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
