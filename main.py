import csv
import os
from PIL import Image
from pyzbar.pyzbar import decode
from uploader import uploader
import socket



def get_product_data():
    """
    Возвращает dict: { barcode: [articule, sex], ... }
    :return:
    """
    with open("positions.csv", encoding='utf-8') as r_file:
        # Хранит dict:  { barcode: [articule, sex] }
        items_csv = {}

        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter=";")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 0
        # Считывание данных из CSV файла
        for row in file_reader:
            if count == 0:
                # Вывод строки, содержащей заголовки для столбцов
                print(f'Файл содержит столбцы: {", ".join(row)}')
            else:
                items_csv[row[3]] = [row[1], row[9]]

            count += 1
        return items_csv


def photos_handler(items_csv):
    """
    Вернет dict c данными:
    { articule: [barcode, sex, [links_to_images, ...] ] }

    :param items_csv:
    :return:
    """

    fotos = os.listdir('fotos')
    fotos.sort()

    hostname = socket. gethostname()
    local_ip = socket. gethostbyname(hostname)

    # Хранит dict:  { articule: [barcode, sex, [links_to_images, ...] ] }
    fotosart = {}
    group = []
    for foto in fotos:
        path = os.path.join('fotos', foto)
        img = Image.open(path)
        dec = decode(img)
        if not dec:
            group.append('https://marketplace2.ru/fotos/'+foto)
        else:
            try:
                barcode = dec[0].data.decode().replace('+', '').lower()
                article = items_csv[barcode][0]
                fotosart[article] = [barcode, items_csv[barcode][1], group]
            finally:
                group = []

    return fotosart


if __name__ == '__main__':
    product_data = get_product_data()
    ready_data = photos_handler(product_data)

    uploader(ready_data)