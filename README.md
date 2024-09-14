# IBM-Hackathon-Migrato
Migrato's idea for the IBM Hackathon 2024

## Elasticsearch local setup
Make sure you have docker desktop installed for this setup

https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
follow the guide on the above linked webpage, Start a single-node cluster

If you followed the setup correctly, we can test the connection. For sending API requests I use Postman.

curl --location --request PUT 'https://127.0.0.1:9200/index_vector' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic ZWxhc3RpYzp4S1Mra25xUUptNkNPMHN5X0txRw==' \
--data '{
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine"
      },
      "my_text" : {
        "type" : "text"
      }
    }
  }
}'

For authorization, use Basic Auth. The username is elastic, the password you just got from the elasticsearch setup. This API request creates a test index. If successfull you should get a "acknowledge: true" back. 
