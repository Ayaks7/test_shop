import requests


def get_product_data(
    products: list
):
    """Запрашиваем данные с сервера продуктов."""
    headers = {'Accept': 'Accept: application/json'}
    params = {
        'products': products
    }
    res = requests.get(
        'http://nginx/catalog/product_data',
        headers=headers,
        json=params
    ).json()
    return res
