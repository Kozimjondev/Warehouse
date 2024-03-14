from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} - {self.code}"


class Material(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ProductMaterials(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.material.name} - {self.quantity}"


class MaterialBatch(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.material.name} - {self.remainder} - {self.price}"
