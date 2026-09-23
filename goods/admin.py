from django.contrib import admin
from goods.models import Categories,Products

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name','quantity','price','discount')
    list_editable = ('quantity','price','discount')
    search_fields = ('name','discount')
    list_filter  = ('discount','quantity')
    fields = ('name','category','slug','description',('price','discount'),'quantity','image')