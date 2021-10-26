from django.db import models
from django.utils.translation import ugettext_lazy as _
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Product(models.Model):
    STATUS_STOCK = 1
    STATUS_NOT_AVAILABLE = 2
    STATUS_SOON = 3
    STATUS_NOT_SALE = 4
    STATUS_CHOICES = (
        (STATUS_STOCK, 'в наличии'),
        (STATUS_NOT_AVAILABLE, 'нет в наличии'),
        (STATUS_SOON, 'скоро будет'),
        (STATUS_NOT_SALE, 'не продается больше')
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.ForeignKey("category.SubCategory", on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    articul = models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default = 1)
    count = models.BigIntegerField(default = 0)
    uuid = models.CharField(max_length=150, blank=True, null=True)
    unit = models.SmallIntegerField(default = 1)

    def __str__(self):
        return self.name

def product_photos_dir(instanse, filename):
    usrnme = f'{instanse.product.id}'
    folder_name = f"{usrnme}/{filename}"
    return folder_name

class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to=product_photos_dir, height_field=None, width_field=None)

    def __str__(self):
        return self.product.name

    def save(self):
        # Opening the uploaded image
        im = Image.open(self.image)
        output = BytesIO()
        # Resize/modify the image
        width, height = im.size
        if width > 1000:
            im = im.resize((width-200, height-200))

        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=90)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(ProductImage, self).save()