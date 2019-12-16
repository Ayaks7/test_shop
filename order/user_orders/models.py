from datetime import datetime
from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, blank=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления", auto_now=True, blank=True
    )
    client_id = models.PositiveIntegerField(
        verbose_name="Идентификатор пользователя", blank=True, null=True
    )
    unique_number = models.CharField(
        verbose_name='Уникальный номер', max_length=64
    )

    def add_products(self, products: list):
        """Добавление продуктов к заказу."""
        uniq_prods = []
        for p in products:
            if not OrderProduct.objects.filter(
                    product_id=p['id'], order=self
            ).exists():
                uniq_prods.append((p['id'], p['count']))

        OrderProduct.objects.bulk_create(
            [
                OrderProduct(
                    order=self,
                    product_id=p[0],
                    product_count=p[1]
                )
                for p in uniq_prods
            ]
        )
        OrderProduct.objects.exclude(
            order=self,
            id__in=[p['id'] for p in products]
        ).delete()

    def save(self, *args, **kwargs):
        """
        При создании объекта добавляем уникальный идентификатор.
        При обновлении проставляем дату апдейта.
        """
        date = datetime.now()
        if self.pk is None:
            last_now_order = self.__class__.objects.filter(
                created_at__date=date,
            ).count()
            self.unique_number = f'{date.date()},№{last_now_order + 1}'
        else:
            self.updated_at = date
        super(Order, self).save(*args, **kwargs)


class OrderProduct(models.Model):
    """Продукты в заказе."""
    product_id = models.IntegerField(verbose_name='Продукт')
    product_count = models.PositiveIntegerField(verbose_name='Количество')
    order = models.ForeignKey(
        Order, verbose_name='Заказ', on_delete=models.CASCADE
    )
