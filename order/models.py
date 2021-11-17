from django.db import models
from django.db.models.fields import BigIntegerField

class Order(models.Model):
    TYPE_ORDER_ORDER = 1
    TYPE_ORDER_PREORDER = 2
    TYPE_ORDER = (
        (TYPE_ORDER_ORDER, 'Розничный'),
        (TYPE_ORDER_PREORDER, 'Оптовый')
    )
    TYPE_STATUS_NEW = 1
    TYPE_STATUS_PRECESSOING = 2
    TYPE_STATUS_END = 3
    TYPE_STATUS_RETURN = 4
    TYPE_STATUS = (
        (TYPE_STATUS_NEW, 'Новый'),
        (TYPE_STATUS_PRECESSOING, 'В обработке'),
        (TYPE_STATUS_END, 'Доставлен'),
        (TYPE_STATUS_RETURN, 'Возврат')
    )
    TYPE_PICKUP = 1
    TYPE_DELIVER = 2
    TYPE_DELIVERY = (
        (TYPE_PICKUP, 'Самовывоз'),
        (TYPE_DELIVER, 'Доставка')
    )
    date = models.DateTimeField(auto_now_add=True)
    # outlet = models.ForeignKey("locations.Outlets", on_delete=models.CASCADE,null=True, blank=True)
    type_order = models.SmallIntegerField(choices=TYPE_ORDER, blank=True, null=True, default = 1)
    status = models.SmallIntegerField(choices=TYPE_STATUS, blank=True, null=True, default = 1)
    courier = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True, related_name='courier')
    delivered_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    counterparty = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True, related_name='conterparty')
    type_delivery = models.SmallIntegerField(choices=TYPE_DELIVERY, blank=True, null=True, default = 1)
    total = models.BigIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        s = self.product_order.all()
        summ = 0
        if len(s) >= 1:
            for i in s:
                if i.count:
                    summ += i.product.price * i.count
                else:
                    summ += i.product.price
        self.total = summ
        super(Order, self).save(*args, **kwargs)


# class Basket(models.Model):
#     user = models.ForeignKey("users.User", on_delete=models.CASCADE)

class OrderProduct(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='order_product')
    count = models.BigIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="product_order")
    # basket = models.ForeignKey(Basket, on_delete=models.CASCADE, null=True, blank=True, related_name="basket_product")

    def __str__(self):
        return f'{self.product.name}'


class Schedule(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    point = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="point_shedule")
    agent = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="agent_shedule")
    plan = models.BooleanField(default=False)
    fact = models.BooleanField(default=False)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f'{self.point.name}, {self.date}'