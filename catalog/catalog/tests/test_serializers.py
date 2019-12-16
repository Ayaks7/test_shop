import pytest

from catalog.models import Product
from catalog.serializers import ProductSerializer


@pytest.mark.parametrize(
    'product, serialize_date',
    [
        (
            Product.get(Product.id == 1),
            {
                'id': 1,
                'name': 'Apple',
                'price': 50

            }
        ),
        (
            Product.get(Product.id == 2),
            {
                'id': 2,
                'name': 'Banana',
                'price': 60

            }
        ),
        (
            Product.get(Product.id == 3),
            {
                'id': 3,
                'name': 'Pear',
                'price': 40

            }
        )
    ]
)
def test_serialize(
    product, serialize_date
):
    """Тестируем сериализатор."""
    serialize_product = ProductSerializer(**getattr(product, '__data__'))
    assert serialize_product == serialize_date
