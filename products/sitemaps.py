from django.contrib.sitemaps import Sitemap
from .models import Brand, Product


class BrandSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # İstersen sadece ürünü olan markaları da döndürebiliriz
        return Brand.objects.order_by("name")

    def location(self, obj):
        # /bmw-yedek-parca/ formatı
        return f"/{obj.slug}-yedek-parca/"


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at
