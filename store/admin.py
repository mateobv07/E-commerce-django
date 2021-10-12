from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'subject', 'rating', 'user', 'updated_date')
    list_filter = ('product', 'rating', 'updated_date')

admin.site.register(Product, ProductAdmin)

admin.site.register(Variation, VariationAdmin)

admin.site.register(ReviewRating, ReviewAdmin)

admin.site.register(ProductGallery)
