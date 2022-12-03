from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    quantity_desc = models.CharField(max_length=20, default=" ")
    desc1 = models.CharField(max_length=300)
    desc2 = models.CharField(max_length=300, default=" ")
    desc3 = models.CharField(max_length=300, default=" ")
    hidden = models.CharField(max_length=300, default=" ")
    categories = models.CharField(max_length=20, default=" ")
    subcategories = models.CharField(max_length=20, default=" ")
    product_image = models.CharField(max_length=50, default=" ")
    discount_price = models.IntegerField(default=0)
    actual_price = models.IntegerField(default=0)
    save_rs = models.CharField(max_length=5, default="n")

    def __str__(self):
        return (self.product_name) + " " + (self.quantity_desc) + " " + (self.subcategories)


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default="")
    address = models.CharField(max_length=600)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=5, default="P")
    total = models.CharField(max_length=10, default="none")

    def __str__(self):
        return (self.name) + " " + str((self.order_id)) + " " + (self.status)
