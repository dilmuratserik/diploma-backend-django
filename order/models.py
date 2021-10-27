from django.db import models

class Order(models.Model):
    TYPE_ORDER_ORDER = 1
    TYPE_ORDER_PREORDER = 2
    TYPE_ORDER = (
        (TYPE_ORDER_ORDER, 'Розничный'),
        (TYPE_ORDER_PREORDER, 'Оптовый')
    )
    TYPE_STATUS_NEW = 1
    TYPE_STATUS_PRECESSOING = 2
    TYPE_STATUS_END = 2
    TYPE_STATUS = (
        (TYPE_STATUS_NEW, 'Новый'),
        (TYPE_STATUS_PRECESSOING, 'В обработке'),
        (TYPE_STATUS_END, 'Доставлен')
    )
    date = models.DateTimeField(auto_now_add=True)
    outlet = models.ForeignKey("locations.Outlets", on_delete=models.CASCADE,null=True, blank=True)
    type_order = models.SmallIntegerField(choices=TYPE_ORDER, blank=True, null=True)
    status = models.SmallIntegerField(choices=TYPE_STATUS, blank=True, null=True, default = 1)
    courier = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True, related_name='courier')
    delivered_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    products = models.ManyToManyField("product.Product")
    counterparty = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True, related_name='conterparty')

    def __str__(self):
        return f'{self.id}, {self.outlet.name}'

    def products_count(self):
        return len(self.products.all())
    

