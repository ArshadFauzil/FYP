from pprint import pprint
import os
import requests

TOKEN = os.getenv('API_TOKEN')
CTYPE = os.getenv('API_CONTENT_TYPE')
print(TOKEN)

url = 'https://api.dialogflow.com/v1/entities/ds_attributes'
url_ds_attributes = 'https://api.dialogflow.com/v1/entities/ds_attributes'
header = {'Authorization': TOKEN, 'content-type': CTYPE}
body = """{
  "entries": [{
      "value": "Name"
    },
    {
      "value": "Age"
    },
    {
      "value": "Salary"
    },
    {
      "value": "Height"
    }
  ],
  "name": "ds_attributes"
}"""

body2 = """{
  "entries": [{
      "value": "9999" 
    }, 
    {
      "value": "restaurant_id" 
    }, 
    {
      "value": "restaurant_name" 
    }, 
    {
      "value": "country_code" 
    }, 
    {
      "value": "city" 
    }, 
    {
      "value": "longitude" 
    }, 
    {
      "value": "latitude" 
    }, 
    {
      "value": "average_cost_for_two" 
    }, 
    {
      "value": "currency" 
    }, 
    {
      "value": "has_table_booking" 
    }, 
    {
      "value": "has_online_delivery" 
    }, 
    {
      "value": "is_delivering_now" 
    }, 
    {
      "value": "switch_to_order_menu" 
    }, 
    {
      "value": "price_range" 
    }, 
    {
      "value": "aggregate_rating" 
    }, 
    {
      "value": "rating_color" 
    }, 
    {
      "value": "rating_text" 
    }, 
    {
      "value": "votes" 
    }, 
    {
      "value": "cuisines" 
    }
  ],
  "name": "ds_attributes"
}"""

dlt_body = """[
              "Age",
              "Name",
              "Height"
              ]"""

# GET Entities
# data = requests.get(url, headers=header)
# pprint(data.json())

# # PUT new entries to entity
# r = requests.put(url, data=body2, headers=header)
# pprint(r.json())

# # DELETE entities
# d = requests.delete(url + '/entries', data=dlt_body, headers=header)
# print(d.json())


# print(body)
url_ds_attributes = 'https://api.dialogflow.com/v1/entities/ds_attributes'
data = ['milan', 'tharindu', 'arshad', 'dinusha', 'ruchira']


def enter_new_entity(entities, url_ds):
    head = """{
  "entries": ["""

    tail = """\n  ],
  "name": "ds_attributes"
}"""

    val = "{\n      \"value\": \"9999\" \n    , \n      \"synonyms\": ['4444'] \n    }"
    val_head = ", \n    {\n      \"value\": \""
    val_tail = "\" "
    entry_tail = "\n    }"

    syn_head = ", \n     \"synonyms\": ["
    syn_tail = "] \n"
    mad = "friend"
    for a in entities:
        entry = val_head + a + val_tail + syn_head + "\"" + mad + "\"" + syn_tail + entry_tail
        val = val + entry

    payload = head + val + tail
    print(payload)
    req = requests.put(url_ds, data=payload, headers=header)
    pprint(req.json())
    print("Entities successfully added")


def enter_new_entity_old(entities, url):
    head = """{
  "entries": ["""

    tail = """\n  ],
  "name": "ds_attributes"
}"""

    val = "{\n      \"value\": \"9999\" \n    },{\n      \"value\": \"4444\" \n    }"
    val_head = ", \n    {\n      \"value\": \""
    val_tail = "\" \n    }"

    syn_head = ", \n    {\n      \"value\": \""
    syn_tail = "\" \n    }"
    print(entities)
    for a in entities:
        entry = val_head + a[0] + val_tail
        synonym = syn_head + a[1] + syn_tail
        val = val + entry + synonym

    payload = head + val + tail
    print(payload)
    r = requests.put(url, data=payload, headers=header)
    pprint(r.json())
    print("Entities successfully added")


if __name__ == '__main__':
    enter_new_entity(data, url_ds_attributes)
