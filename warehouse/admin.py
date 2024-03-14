from django.contrib import admin

from .models import Product, Material, ProductMaterials, MaterialBatch


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductMaterials)
class ProductMaterialsAdmin(admin.ModelAdmin):
    list_display = ('product', 'material', 'quantity')


@admin.register(MaterialBatch)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('material', 'remainder', 'price')
