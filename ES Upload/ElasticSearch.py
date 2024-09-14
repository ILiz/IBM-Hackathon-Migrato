import requests

import Credentials


def send_data(ind, text, dense_vector, sparse_vector, title, uri_source):
    requests.post(url=Credentials.url + Credentials.index + Credentials.add_document + str(ind), json={
        "my_vector": dense_vector.tolist(),
        "my_sparse_vector": sparse_vector.toarray().tolist()[0],
        "my_text": text,
        "my_title": title,
        "my_uri_source": uri_source
    },
                  auth=(Credentials.authentication_username, Credentials.authentication_password))


def send_data_bulk(bulk_data):
    r = requests.post(url=Credentials.url + Credentials.index + "/_bulk",
                      data=bulk_data.encode("utf-8"),
                      auth=(Credentials.authentication_username, Credentials.authentication_password),
                      headers={'Content-Type': 'application/x-ndjson'}
                      )
    if r.json()['errors']:
        print(r.content)


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
                "my_sparse_vector": {
                    "type": "dense_vector"
                },
                "my_text": {
                    "type": "text"
                },
                "my_title": {
                    "type": "text"
                },
                "my_uri_source": {
                    "type": "text"
                },
                "my_extension": {
                    "type": "text"
                },
                "my_creation_date": {
                    "type": "text"
                },
                "my_numpages": {
                    "type": "text"
                },
                "my_author": {
                    "type": "text"
                }
            }
        }
    }, auth=(Credentials.authentication_username, Credentials.authentication_password))
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


def delete_index():
    requests.delete(url=Credentials.url + Credentials.index,
                    auth=(Credentials.authentication_username, Credentials.authentication_password))
