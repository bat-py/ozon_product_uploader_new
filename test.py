import json
import requests

def get_header():
    """
    Из файла config.ini берет Client-Id и Api-Key. Вернет библиотеку header = {'Client-Id': data[0], 'Api-Key': data[1]}
    """

    with open('config.ini') as conf:
        config = conf.readlines()

        data = [i.split('=')[1].strip().replace('"', '') for i in config]
        header = {'Client-Id': data[0], 'Api-Key': data[1], 'Content-type': 'application/json'}

        return header


def post_request(json_data):
    header = get_header()
    a = {"attribute_type": "REQUIRED",
         "category_id": [17038455],
         "language": 'DEFAULT'
         }

    req = requests.post('https://api-seller.ozon.ru/v2/product/import', headers=header, data=json_data.encode('utf-8'))
    print(req.text)


if __name__ == '__main__':
    jsonn = {
        "items": [

            {

                "attributes": [
                    {
                        "complex_id": 0,
                        "id": 85,
                        "values": [
                            {
                                "dictionary_value_id": 28732849,
                                "value": 'POLARIZED'
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
                           "value": "X8215-1 солнцезащитные"}]},
                    {"id": 9725, "complex_id": 0,
                     "values":
                         [{"dictionary_value_id": 970867649,
                           "value": "Весна-Лето 2021"}]},
                    {"id": 9163, "complex_id": 0,
                     "values": [{"dictionary_value_id": 22880,
                                 "value": "Мужской"}]},

                ],
                "barcode": "TTT310462866",
                "category_id": 17038455,
                "depth": 200,
                "dimension_unit": "mm",
                "height": 70,
                # "image_group_id": "string",
                "images": [
                    "https://optictrend.ru/upload/iblock/92b/92b3c2f3e4cd5fd1250013f01b3bfb59.png"
                ],
                "name": "Очки мужские солнцезащитные",
                "offer_id": "X8215-1",
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

    json_data = json.dumps(jsonn, ensure_ascii=False)
    post_request(json_data)