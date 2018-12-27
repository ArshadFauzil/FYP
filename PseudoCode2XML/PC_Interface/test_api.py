from pprint import pprint
import os
import requests

TOKEN = os.getenv('API_TOKEN')
CTYPE = os.getenv('API_CONTENT_TYPE')
print(TOKEN)

url = 'https://api.dialogflow.com/v1/entities/ds_attributes'
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

# PUT new entries to entity
r = requests.put(url, data=body2, headers=header)
pprint(r.json())

# # DELETE entities
# d = requests.delete(url + '/entries', data=dlt_body, headers=header)
# print(d.json())


print(body)