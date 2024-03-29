from django.db import models
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _
# from django.core.mail import send_mail
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
# from django.contrib.postgres.fields import ArrayField
# from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
# from datetime import datetime
# from io import BytesIO
# from PIL import Image
# from django.core.files.uploadedfile import InMemoryUploadedFile

TYPE_PRICE_RETAIL = 1
TYPE_PRICE_WHOSALE = 2
TPE_PRICE_SPEC = 3
TYPE_PRICES = (
    (TYPE_PRICE_RETAIL, 'Розничный'),
    (TYPE_PRICE_WHOSALE, 'Оптовый'),
    (TPE_PRICE_SPEC, 'Спец.цена')
)
class Company(models.Model):
    name = models.CharField(max_length=150)
    bin = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    type_price = models.ForeignKey('settings.Type_Price', blank=True, null=True, on_delete=models.PROTECT)
    fio = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, phone):
        if not phone:
            raise ValueError(_("Users must have an phone address"))
        # email = self.normalize_email(email)
        user = self.model(phone=phone)
        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password,**extra_fields):
        user = self.create_user(phone)
        # user.is_active = True
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        # user.role = User.ROLE_ADMINISTRATOR
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, password=None):
        user = self.create_user(phone, password=password, is_staff=True, is_active=True)
        return user


def user_photos_dir(instanse, filename):
    usrnme = f'{instanse.phone}'
    folder_name = f"{usrnme}/{filename}"
    return folder_name


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_INDIVIDUAL = 1
    ROLE_ORGANIZATION = 2
    ROLE_TP = 3
    ROLE_COURIER = 4
    ROLE_CHOICES = (
        (ROLE_INDIVIDUAL, 'Физическое лицо'),
        (ROLE_ORGANIZATION, 'Организация'),
        (ROLE_TP, 'Торговый представитель'),
        (ROLE_COURIER, 'Курьер')
    )
    
    ORDER_SECTOR_BEER = 1
    ORDER_SECTOR_SHOP = 2
    ORDER_SECTOR_SUPERMARKET = 3
    ORDER_SECTORS = (
        (ORDER_SECTOR_BEER, 'Пивнушка'),
        (ORDER_SECTOR_SHOP, 'Магазин'),
        (ORDER_SECTOR_SUPERMARKET, 'Супермаркет')
    )

    phone_regex = RegexValidator( regex = r'^\+?1?\d{7,12}$',
                                  message = "Phone number in the format '+77777777'. Up to 12 digits")
    phone = models.CharField(max_length=12,validators = [phone_regex], unique=True)
    # phone = models.CharField(max_length=15, unique=True)
    password1 = models.CharField(max_length=20, blank=True, null=True)
    password2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    # nickname = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)

    birth_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    bin_iin = models.CharField(max_length=50, blank=True, null=True)
    # ------------------------------------------------------
    country = models.ForeignKey("locations.Country", on_delete=models.CASCADE, blank=True, null=True)
    # region = models.ForeignKey("locations.Region", on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey("locations.City", on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey("locations.Location", on_delete=models.CASCADE, blank=True, null=True)
    # -------------------------------------------------------
    role = models.SmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    type_price = models.SmallIntegerField(choices=TYPE_PRICES, blank=True, null=True)
    price_type = models.ForeignKey('settings.Type_Price', blank=True, null=True, on_delete=models.PROTECT)
    sector_order = models.ForeignKey('settings.Order_Sector', blank=True, null=True, on_delete=models.PROTECT)
    storage = models.ForeignKey("locations.Storage_region", on_delete=models.CASCADE, blank=True, null=True)
    order_sector = models.SmallIntegerField(choices=ORDER_SECTORS, blank=True, null=True)
    #--------------------------------------------------------
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_checked = models.BooleanField(default=False)
    is_moder = models.BooleanField(default=False)
    #--------------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to=user_photos_dir, default="default/default.jpg")
    # -------------------------------------------------------

    credit = models.CharField(max_length = 300, null=True, blank=True)
    paymets = models.IntegerField(default=0)
    galleon = models.BooleanField(default=True)
    debt = models.IntegerField(default=0)
    agent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    bonus = models.BigIntegerField(default = 0)

    show_plan = models.IntegerField(default=24, blank=True)
    show_plan_date = models.DateTimeField(auto_now=True)
    working_hour_with = models.CharField(max_length=50, null=True, blank=True)
    working_hour_until = models.CharField(max_length=50, null=True, blank=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return str(self.id) + ", " + self.phone

    
    # def save(self, *args, **kwargs):
    #     # Opening the uploaded image
    #     print(self.avatar.name.split('.')[0])
    #     if self.avatar and self.avatar.name.split('.')[0] != 'default/default.png':
    #         im = Image.open(self.avatar)
    #         output = BytesIO()
    #         # Resize/modify the image
    #         width, height = im.size
    #         if width > 1000:
    #             im = im.resize((width-200, height-200))

    #         # after modifications, save it to the output
    #         im.save(output, format='JPEG', quality=90)
    #         output.seek(0)

    #         # # change the imagefield value to be the newley modifed image value
    #         # print(self.avatar.name.split('.')[0])
    #         self.avatar = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.avatar.name.split('.')[0], 'image/jpeg',
    #                                         sys.getsizeof(output), None)
    #         super(User, self).save()

    def locations(self):
        if self.country:
            return self.country.name + ', ' + self.city.name
        else:
            return ""



class PhoneOTP(models.Model):
    # phone_regex = RegexValidator( regex = r'^\+?1?\d{7,12}$',
    # message = "Phone number in the format '+77777777'. Up to 12 digits")
    # phone = models.CharField(max_length=12,validators = [phone_regex], unique=True)
    phone = models.CharField(max_length = 12, unique = True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    validated = models.BooleanField(default=False, help_text = 'True means user has a validated otp correctly in second API')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
