from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .forms import CategoryForm

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(ModelProduct)
admin.site.register(ImagesProduct)
admin.site.register(Customer)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'category_icon')
    list_display_links = ('title', )
    prepopulated_fields = {'slug': ('title', )}
    form = CategoryForm

    def category_icon(self, obj):
        if obj.icon:
            try:
                return mark_safe(f'<img src="{obj.icon.url}" width="30" >')
            except:
                return 'no icon'
        else:
            return 'no icon'

    category_icon.short_description = 'Иконка'


class ImagesProductInLine(admin.TabularInline):
    model = ImagesProduct
    fk_name = 'product'
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'quantity', 'model', 'discount', 'price', 'product_image')
    list_display_links = ('title', )
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImagesProductInLine]
    list_filter = ('quantity', 'discount', 'price', 'category')
    list_editable = ('quantity', 'discount', 'price', )

    def product_image(self, obj):
        if obj.images.exists():
            try:
                return mark_safe(f'<img src="{obj.images.first().image.url}" width="60" >')
            except:
                return 'no image'
        else:
            return 'no image'

    product_image.short_description = 'Фото товара'



@admin.register(ModelProduct)
class ModelProductAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    prepopulated_fields = {'slug': ('title', )}

