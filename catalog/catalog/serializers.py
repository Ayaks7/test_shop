from pydantic import BaseModel


class ProductSerializer(BaseModel):
    """Заготовка для сериализации модели Product."""
    id: int
    name: str
    price: int
