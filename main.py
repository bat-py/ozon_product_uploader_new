import csv
import os
from PIL import Image
from pyzbar.pyzbar import decode
from uploader import uploader
import configparser
import shutil

config = configparser.ConfigParser()
config.read('config.ini')


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

    # Проверяем 1 фото это штрихкод или нет
    fist_photo = os.path.join('fotos', fotos[0])
    img = Image.open(fist_photo)
    decoded = decode(img)

    # Если сперва идут фото со штрихкодом, потом фотографии товаров:
    if decoded:
        # Хранит dict:  { articule: [barcode, sex, [links_to_images, ...] ] }
        fotosart = {}

        # Станет True если найденный штрихкод в фото нету в csv файле, после этого скприт будет пропускать все фото этого продукта
        barcode_not_in_csv = False
        for foto in fotos:
            path = os.path.join('fotos', foto)
            img = Image.open(path)
            dec = decode(img)

            # Если нашел фото с штрихкодом, тогда создает новый dict элемент в fotosart
            if dec:
                try:
                    barcode_not_in_csv = False

                    barcode = dec[0].data.decode().replace('+', '').lower()
                    article = items_csv[barcode][0]
                    fotosart[article] = [barcode, items_csv[barcode][1], []]
                except:
                    barcode_not_in_csv = True

                    barcode = dec[0].data.decode().replace('+', '').lower()
                    print(f'Штрихкод {barcode} не найден в csv файле!')

            # Если фото без штрихкода, тогда добавляет ссылки на фото в последный элемент fotosart
            else:
                # Если штрихкод товара не найден в csv файле, все фото этого товара пропустим
                if barcode_not_in_csv:
                    continue
                # Добавим ссылку на фото в последный элемент dict "fotosart[2]"
                fotosart[list(fotosart.keys())[-1]][2].append(config['DOMAIN']['domain_name'] + 'fotos/' + foto)

        return fotosart

    # Если сперва идут фотографии товаров а потом штрихкод товара:
    else:
        # Хранит dict:  { articule: [barcode, sex, [links_to_images, ...] ] }
        fotosart = {}
        group = []
        for foto in fotos:
            path = os.path.join('fotos', foto)
            img = Image.open(path)
            dec = decode(img)
            if not dec:
                group.append(config['DOMAIN']['domain_name'] + 'fotos/' + foto)
            else:
                try:
                    barcode = dec[0].data.decode().replace('+', '').lower()
                    article = items_csv[barcode][0]
                    fotosart[article] = [barcode, items_csv[barcode][1], group]
                except:
                    barcode = dec[0].data.decode().replace('+', '').lower()
                    print(f'Штрихкод {barcode} не найден в csv файле!')
                finally:
                    group = []

        return fotosart


def image_creator_to_upload(ready_data):
    # Проверяем есть ли папка fotos_to_upload, если нету создадим, если есть удаляем все файлы внутри него
    if os.path.isdir('fotos_to_upload'):
        trash_files = os.listdir('fotos_to_upload')

        for file in trash_files:
            os.remove('fotos_to_upload/'+file)
    else:
        os.mkdir('fotos_to_upload')

    # Получаем имя домена из config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config['DOMAIN']['domain_name']

    for article, data in ready_data.items():
        photo_num = 0

        for photo in data[2]:
            old_photo_link = photo.replace(url, '')
            photo_extension = old_photo_link.split('.')[1]
            new_photo_path = 'fotos_to_upload/'

            if photo_num == 0:
                shutil.copy2(old_photo_link, f'{new_photo_path}{article.strip()}.{photo_extension}')
                photo_num += 2
            else:
                shutil.copy2(old_photo_link, f'{new_photo_path}{article.strip()}_{str(photo_num)}.{photo_extension}')
                photo_num += 1


if __name__ == '__main__':
    product_data = get_product_data()

    # Получает dict типа: { articule: [barcode, sex, [links_to_images, ...] ] }
    ready_data = photos_handler(product_data)

    # В папке fotos_to_upload создаем фотографии с названием артикула для загрузки вручную
    image_creator_to_upload(ready_data)
    print(ready_data)
    #uploader(ready_data)