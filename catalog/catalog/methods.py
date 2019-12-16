from catalog import app
from catalog.models import Product
from catalog.serializers import ProductSerializer


@app.get("/catalog/product_data")
async def get_product_data(
    data: dict
):
    """Получение списка продуктов из заказа."""
    order_products = {
        x['product_id']: {'product_count': x['product_count']}
        for x in data['products'] if x['product_count'] > 0
    }

    # Получаем продукты по id из БД
    products = await Product.get_objects_by_id([p for p in order_products])

    # Формируем итоговые данные, исходя из кол-ва запрошенных продуктов
    order_price = 0
    for product in products:
        full_price = order_products[product.id]['product_count'] * product.price
        order_products[product.id]['name'] = product.name
        order_products[product.id]['price'] = product.price
        order_products[product.id]['full_price'] = full_price
        order_price += full_price

    return order_products, order_price


@app.get("/catalog/all")
async def get_all_products():
    """Получение списка всех продуктов."""
    products = await Product.get_objects()
    products_data = list()
    for product in products:
        serialize_data = ProductSerializer(
            **getattr(product, '__data__')
        )
        products_data.append(serialize_data)
    return products_data
