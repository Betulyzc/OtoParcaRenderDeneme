from django.contrib import admin
from .models import Product, Category, Brand


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "oem_code", "featured", "created_at")
    list_filter = ("brand", "category", "featured")
    search_fields = ("name", "oem_code", "compatible")
    list_select_related = ("brand", "category")  # performans
    ordering = ("-created_at",)

    # Slug otomatik dolsun ama biz zaten models.py'de güvenli üretiyoruz.
    # Yine de admin'de önizleme için kalsın:
    prepopulated_fields = {"slug": ("name",)}

    autocomplete_fields = ("brand", "category")

    # Admin formunda alanları daha düzenli gösterelim
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "category", "brand", "oem_code", "compatible", "short_desc")
        }),
        ("Medya / Link", {
            "fields": ("image",)
        }),
        ("Öne Çıkan / Tarih", {
            "fields": ("featured", "created_at")
        }),
    )
    readonly_fields = ("created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
