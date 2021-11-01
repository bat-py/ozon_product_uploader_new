import requests
import json
import configparser
import configparser

def get_header():
    """
    Из файла config.ini берет Client-Id и Api-Key. Вернет библиотеку header = {'Client-Id', 'Api-Key', 'Content-type'}
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    data = config['HEADERS']

    header = {'Client-Id': int(data['Client-Id']), 'Api-Key': data['Api-Key'], 'Content-type': 'application/json'}
    return header


def post_request(json_data):
    header = get_header()

    req = requests.post('https://api-seller.ozon.ru/v2/product/import', headers=header, data=json_data.encode('utf-8'))
    print(req.text)


def uploader(data, photo_upload_method):
    # в data есть dict:  { articule: [barcode, sex, [links_to_images, ...] ] }
    config = configparser.ConfigParser()
    config.read('config.ini')

    season = config['TOVARS_DATA']['season']
    brand = config['TOVARS_DATA']['brand']

    i = 0
    for article, datas in data.items():
        if i > 3:
            break
        i += 1

        if datas[1].lower().strip() == 'мужской':
            sex_for_name = 'Мужские очки'
            category_id = 17038455
        elif datas[1].lower().strip() == 'женский':
            sex_for_name = 'Женские очки'
            category_id = 78302015
        elif datas[1].lower().strip() == 'женский, мужской' or datas[1].lower().strip() == 'мужской, женский':
            sex_for_name = 'Очки Унисекс'
            category_id = 85848444
        else:
            sex_for_name = 'Мужские очки'
            category_id = 17038455

        if photo_upload_method == 1:
            images = datas[2]
        else:
            images = []

        json_data = {
            "items": [

                {
                    "attributes": [
                        {
                            "complex_id": 0,
                            "id": 85,
                            "values": [
                                {
                                    "dictionary_value_id": 28732849,
                                    "value": f'{brand}'
                                }
                            ]
                        },
                        {
                            "complex_id": 0,
                            "id": 8229,
                            "values": [
                                {
                                    "dictionary_value_id": 93866,
                                    "value": 'Очки солнцезащитные'
                                }
                            ]
                        },

                        {"id": 9048, "complex_id": 0,
                         "values":
                             [{"dictionary_value_id": 0,
                               "value": f"{article} солнцезащитные"}]},

                        {"id": 9725, "complex_id": 0,
                         "values":
                             [{"dictionary_value_id": 970867649,
                               "value": f"{season}"}]},

                        {"id": 9163, "complex_id": 0,
                         "values": [{"dictionary_value_id": 22880,
                                     "value": f"{datas[1]}"}]},

                    ],
                    "barcode": f"{datas[0]}",
                    "category_id": category_id,
                    "depth": 200,
                    "dimension_unit": "mm",
                    "height": 70,
                    "images": images,
                    "name": f"{sex_for_name} {season} {brand}",
                    "offer_id": f"{article.strip()}",
                    "old_price": "1000",
                    "premium_price": "750",
                    "price": "800",
                    "vat": "0",
                    "weight": 100,
                    "weight_unit": "g",
                    "width": 100
                }
            ]

        }

        ready_json = json.dumps(json_data, ensure_ascii=False, )
        print(ready_json)
        post_request(ready_json)

    print(f'Создано {str(len(data))} товаров!')



