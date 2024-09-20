import requests

from Backend.libs import Credentials


def send_data_bulk(bulk_data):
    r = requests.post(url=Credentials.url + Credentials.index + "/_bulk",
                      data=bulk_data.encode("utf-8"),
                      auth=(Credentials.authentication_username, Credentials.authentication_password),
                      headers={'Content-Type': 'application/x-ndjson'},
                      verify=False
                      )
    if r.json()['errors']:
        print(r.content)

