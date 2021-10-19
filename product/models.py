from django.db import models
from django.utils.translation import ugettext_lazy as _
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE)
    subcategory = models.ForeignKey("category.SubCategory", on_delete=models.CASCADE)
    price = models.IntegerField()
    weight = models.IntegerField()

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