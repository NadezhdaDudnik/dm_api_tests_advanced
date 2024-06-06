"""curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "Nadin",
  "email": "nadin_email@mail.ru",
  "password": "123456789"
}'"""
"""
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/499709ad-a7a4-49fe-92af-71261dfe9875' \
  -H 'accept: text/plain'"""

import pprint

import requests

#
# url = "http://5.63.153.31:5051/v1/account"
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# json = {
#     "login": "Nadin1",
#     "email": "nadin_email1@mail.ru",
#     "password": "123456789"
# }
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )
#
# print(response.status_code)
# print(response.json())
# # pprint.pprint(response.json())

url = "http://5.63.153.31:5051/v1/account/499709ad-a7a4-49fe-92af-71261dfe9875"
headers = {
    'accept': 'text/plain',
}
response = requests.put(
    url=url,
    headers=headers
)
print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])
