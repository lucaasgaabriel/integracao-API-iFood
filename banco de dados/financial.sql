create table consumo_ifood.financial
(
    cod_pedido     varchar(50) null,
    order_type     varchar(30) null,
    nome_loja      varchar(50) null,
    item_venda     varchar(50) null,
    qtd_item_venda int         not null,
    preco_item     double      null,
    delivery_fee   double      null,
    benefits       double      null,
    subtotal_venda double      null,
    metodo_pg      varchar(30) null
);

