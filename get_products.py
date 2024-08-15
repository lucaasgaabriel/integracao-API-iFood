import requests
from authentication import *
from db_connect import *

authentication = import_token()
access_token = authentication[0]
merchant_uuid = authentication[1]
catalog_uuid = authentication[2]

db_connect = connect_sql()
connection = db_connect[0]
cursor = db_connect[1]

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(f"https://merchant-api.ifood.com.br/catalog/v2.0/merchants/{merchant_uuid}/catalogs"
                        f"/{catalog_uuid}/categories",
                        headers=headers)

data = response.json()

for name in data:
    category_name = name.get("name")

    for item in name.get("items", []):
        id_produto = item.get("productId")
        nome_produto = item.get("name")
        preco_produto = item.get("price").get("value")

        insert_query = "INSERT INTO produtos (id_produto, nome_produto, preco_produto, categoria_produto) VALUES (%s, %s, %s, %s)"
        values = (id_produto, nome_produto, preco_produto, category_name)

        cursor.execute(insert_query, values)
        connection.commit()

cursor.close()
connection.close()
