import pytest
from starlette.testclient import TestClient

from catalog import app
from catalog.methods import get_product_data


client = TestClient(app)


def test_response():
    """Тест ответа сервера."""
    response = client.get("/catalog/all")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_data, product_data',
    [
        (
            {
                'products': [
                    {"product_id": 1, "product_count": 2}
                ]
            },
            (
                {
                    1: {
                        'product_count': 2,
                        'name': 'Apple',
                        'price': 50,
                        'full_price': 100
                        }
                }, 100
            )
        ),
        (
            {
                'products': [
                    {"product_id": 3, "product_count": 7}
                ]
            },
            (
                {
                    3: {
                        'product_count': 7,
                        'name': 'Pear',
                        'price': 40,
                        'full_price': 280
                        }
                }, 280
            )
        ),
        (
            {
                'products': [
                    {"product_id": 3, "product_count": 7},
                    {"product_id": 2, "product_count": 14},
                ]
            },
            (
                {
                    3: {
                        'product_count': 7,
                        'name': 'Pear',
                        'price': 40,
                        'full_price': 280
                        },
                    2: {
                        'product_count': 14,
                        'name': 'Banana',
                        'price': 60,
                        'full_price': 840
                        }
                    }, 1120
            )
        ),
    ]
)
async def test_get_products(
    test_data, product_data, event_loop
):
    """Тестируем итоговые данные по запросу продктов."""
    data = await get_product_data(test_data)
    assert data == product_data
