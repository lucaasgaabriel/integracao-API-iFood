import requests
from datetime import datetime
from authentication import *
from db_connect import *

authentication = import_token()
access_token = authentication[0]
merchant_uuid = authentication[1]

db_connect = connect_sql()
connection = db_connect[0]
cursor = db_connect[1]

url = "https://merchant-api.ifood.com.br/order/v1.0/events:polling?types=PLC%2CREC%2CCFM&groups=ORDER_STATUS%2CDELIVERY"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)
data = response.json()

order_id = []

for code in data:
    order_id.append(code.get('orderId'))
    order_code = code.get('fullCode')
    merchant_id = code.get('merchantId')

for cod in order_id:
    url_order = f"https://merchant-api.ifood.com.br/order/v1.0/orders/{cod}"

    #Pedido
    response_order = requests.get(url_order, headers=headers)
    order_data = response_order.json()
    order_type = order_data.get('orderType')
    merchant_name = order_data.get('merchant').get('name')
    items = order_data.get('items')
    total_subtotal = order_data.get('total').get('subTotal')
    total_delivery_fee = order_data.get('total').get('deliveryFee')
    total_benefits = order_data.get('total').get('benefits')
    payment_methods_data = order_data.get('payments').get('methods')
    
    # Endereço
    delivery_data = order_data.get('delivery')
    delivery_datetime = delivery_data.get('deliveryDateTime')
    delivery_observations = delivery_data.get('observations')
    delivery_address = delivery_data.get('deliveryAddress')
    street_name = delivery_address.get('streetName')
    street_number = delivery_address.get('streetNumber')
    formatted_address = delivery_address.get('formattedAddress')
    neighborhood = delivery_address.get('neighborhood')
    complement = delivery_address.get('complement')
    postal_code = delivery_address.get('postalCode')
    city = delivery_address.get('city')
    state = delivery_address.get('state')
    country = delivery_address.get('country')
    reference = delivery_address.get('reference')

    # Item
    for item in items:
        items_name = item.get('name')
        items_qtd = item.get('quantity')
        items_price = item.get('price')
        items_priceUnit = item.get('unitPrice')
        items_totalPrice = item.get('totalPrice')

        # Método de pagamento por item
        for method in payment_methods_data:
            payment_value = method.get('value')
            payment_currency = method.get('currency')
            payment_methods = method.get('method')
            payment_type = method.get('type')
            card_brand = method.get('card').get('brand')

            formatted_delivery_datetime = datetime.strptime(delivery_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")

            insert_query = ("INSERT INTO financial (cod_pedido, "
                        "order_type, "
                        "nome_loja, "
                        "item_venda, "
                        "qtd_item_venda, "
                        "preco_item, "
                        "delivery_fee, "
                        "benefits, "
                        "subtotal_venda, "
                        "metodo_pg, "
                        "preco_unidade, "
                        "valor_total, "
                        "total_preco, "
                        "tipo_cartao, "
                        "delivery_datetime, "
                        "delivery_observations, "
                        "street_name, "
                        "street_number, "
                        "formatted_address, "
                        "neighborhood, "
                        "complement, "
                        "postal_code, "
                        "city, "
                        "country, "
                        "reference) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)")
            values = (cod, order_type, merchant_name, items_name, items_qtd, items_price,
                    total_delivery_fee, total_benefits, total_subtotal, payment_methods, items_priceUnit, payment_value, items_totalPrice, card_brand, formatted_delivery_datetime, delivery_observations, street_name, street_number, formatted_address, neighborhood, complement, postal_code, city, country, reference)

            cursor.execute(insert_query, values)
            connection.commit()

cursor.close()
connection.close()