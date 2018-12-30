from pprint import pprint
import os
import requests

TOKEN = os.getenv('API_TOKEN')
CTYPE = os.getenv('API_CONTENT_TYPE')

header = {'Authorization': TOKEN, 'content-type': CTYPE}


def enter_new_entity(entities, url):
    head = """{
  "entries": ["""

    tail = """\n  ],
  "name": "ds_attributes"
}"""

    val = "{\n      \"value\": \"9999\" \n    },{\n      \"value\": \"4444\" \n    }"
    val_head = ", \n    {\n      \"value\": \""
    val_tail = "\" \n    }"
    for a in entities:
        entry = val_head + a + val_tail
        val = val + entry

    payload = head + val + tail
    print(payload)
    r = requests.put(url, data=payload, headers=header)
    pprint(r.json())
    print("Entities successfully added")


def enter_filename_entity(entities, url):
    head = """{
  "entries": ["""

    tail = """\n  ],
  "name": "Dataset_Name"
}"""

    val = "{\n      \"value\": \"9999\" \n    },{\n      \"value\": \"4444\" \n    }"
    val_head = ", \n    {\n      \"value\": \""
    val_tail = "\" \n    }"
    for a in entities:
        entry = val_head + a + val_tail
        val = val + entry

    payload = head + val + tail
    print(payload)
    r = requests.put(url, data=payload, headers=header)
    pprint(r.json())
    print("Entities successfully added")


def delete_entries(entities, url):
    body = """[\"9999\""""
    for a in entities:
        body = body+",\""+a+"\""

    payload = body+"]"

    print(payload)
    d = requests.delete(url + '/entries', data=payload, headers=header)
    print(d.json())


if __name__ == '__main__':
    attributes = ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'longitude', 'latitude',
                  'average_cost_for_two', 'currency', 'has_table_booking', 'has_online_delivery', 'is_delivering_now',
                  'switch_to_order_menu', 'price_range', 'aggregate_rating', 'rating_color', 'rating_text', 'votes',
                  'cuisines']
    url_ds_attributes = 'https://api.dialogflow.com/v1/entities/ds_attributes'

    # enter_new_entity(attributes, url_ds_attributes)
    delete_entries(attributes, url_ds_attributes)
