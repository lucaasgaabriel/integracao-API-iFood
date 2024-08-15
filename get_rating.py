import requests
from authentication import *
from db_connect import *

authentication = import_token()
access_token = authentication[0]
merchant_uuid = authentication[1]

db_connect = connect_sql()
connection = db_connect[0]
cursor = db_connect[1]

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

params = {
    "page": "1",
    "size": "10",
    "reviews": []
}

response = requests.get(f"https://merchant-api.ifood.com.br/review/v1.0/merchants/{merchant_uuid}"
                        "/reviews?page=1&pageSize=10&addCount=false&dateFrom=2023-07-01T00%3A01%3A00Z&dateTo=2023-09"
                        "-01T23%3A59%3A59Z&sort=DESC&sortBy=CREATED_AT", headers=headers, params=params)

data = response.json()

for review in data.get("reviews", []):
    id_review = review.get("id")
    score = review.get("score")
    data_criacao = review.get("createdAt")

    insert_query = "INSERT INTO rating (id_review, score, data_criacao) VALUES (%s, %s, %s)"
    values = (id_review, score, data_criacao)

    cursor.execute(insert_query, values)
    connection.commit()

cursor.close()
connection.close()
