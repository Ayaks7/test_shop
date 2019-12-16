from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer

from user_orders.utils import get_user_id
from user_orders.client import get_product_data
from user_orders.models import Order, OrderProduct


class OrderResource(ModelResource):
    class Meta:
        queryset = Order.objects.all()
        authorization = Authorization()
        allowed_methods = ['get', 'post']
        serializer = Serializer(['json'])

    def dispatch(self, request_type, request, **kwargs):
        """Получение идентификатор пользователя."""
        token = request.META.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        kwargs['client_id'] = get_user_id(token)
        return super().dispatch(request_type, request, **kwargs)

    def obj_create(self, bundle, request=None, **kwargs):
        """Создание объекта заказа с пришедшими данными."""
        data = bundle.data
        products = data.get('products', [])
        client_id = kwargs['client_id']

        # Проверяем наличие заказа у клиента, либо создаем, либо апдейтим
        client_order = Order.objects.filter(client_id=client_id).first()
        if client_order:
            client_order.add_products(products)
            kwargs['obj'] = client_order
            return self.obj_update(bundle, request=request, **kwargs)
        bundle = super().obj_create(bundle, request=request, **kwargs)
        bundle.obj.client_id = client_id
        bundle.obj.save()
        bundle.obj.add_products(products)
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        """Обновление объекта."""
        bundle.obj = kwargs['obj']
        return super().obj_update(bundle, request=request, **kwargs)

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def dehydrate(self, bundle):
        """Формируем данные для ответа."""
        data = bundle.data

        products = OrderProduct.objects.filter(
            order__id=data['id']
        ).values('product_id', 'product_count')
        products = get_product_data(list(products))
        data['products'] = products
        return bundle

    def obj_get_list(self, request=None, **kwargs):
        """Фильтруем заказы по пользователю."""
        return self.get_object_list(request).filter(
            client_id=kwargs['client_id']
        )
