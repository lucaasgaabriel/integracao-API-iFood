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

response_merchant = requests.get("https://merchant-api.ifood.com.br/merchant/v1.0/merchants?page=1&size=100", headers=headers)
data_merchant = response_merchant.json()

response_rating = requests.get(f"https://merchant-api.ifood.com.br/review/v1.0/merchants/{merchant_uuid}/summary",headers=headers)
data_rating = response_rating.json()

for row in data_merchant:
    id_loja = row.get("id")
    nome_loja = row.get("name")

    insert_query = "INSERT INTO loja_geral (id_loja, nome_loja) VALUES (%s, %s)"
    values = (id_loja, nome_loja)

    cursor.execute(insert_query, values)
    connection.commit()

for rating in data_rating:
    total_review = rating.get("totalReviewsCount")
    count_valid = rating.get("validReviewsCount")
    score = rating.get("score")

    insert_query_rating = "INSERT INTO loja_geral(qtd_review, qtd_review_validos, nota_geral) VALUES (%s, %s, %s)"
    values_rating = (total_review, count_valid, score)

    cursor.execute(insert_query_rating, values_rating)
    connection.commit()

cursor.close()
connection.close()
