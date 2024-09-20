import requests

from Backend.libs import Credentials


def send_data_bulk(bulk_data):
    r = requests.post(url=Credentials.url + Credentials.index + "/_bulk",
                      data=bulk_data.encode("utf-8"),
                      auth=(Credentials.authentication_username, Credentials.authentication_password),
                      headers={'Content-Type': 'application/x-ndjson'},
                      verify=False
                      )
    try:
        if r.json()['errors']:
            print(r.content)
    except:
        print(r.json())


def create_index():
    print(Credentials.url + Credentials.index)
    r = requests.put(url=Credentials.url + Credentials.index, json={
        "mappings": {
            "properties": {
                "my_vector": {
                    "type": "dense_vector",
                    "dims": 1024,
                    "index": "true",
                    "similarity": "cosine"
                },
                "Text": {
                    "type": "text"
                },
                "Title": {
                    "type": "text"
                },
                "Course": {
                    "type": "text"
                }
            }
        }
    }, auth=(Credentials.authentication_username, Credentials.authentication_password), verify=False)
    try:
        if r.json()['error']:
            if r.json()['error']['root_cause'][0]['type'] == "resource_already_exists_exception":
                print("index exists")
                return False
            print(r.content)
            return False
    except KeyError:
        print("")
    print("index created")
    return True
