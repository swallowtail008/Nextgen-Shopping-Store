from django.contrib import admin

from .models import *

admin.site.register(Slider)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SIZE)
admin.site.register(COLOR)
admin.site.register(CONDITION)
admin.site.register(Cart)
admin.site.register(Order)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','posted_by','created_at','update_at')

admin.site.register(Product, ProductAdmin)
admin.site.register(Super_SubCategory)
