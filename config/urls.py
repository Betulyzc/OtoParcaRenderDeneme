from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

from products import views as v
from products.sitemaps import BrandSitemap, ProductSitemap

sitemaps = {
    "brands": BrandSitemap,
    "products": ProductSitemap,
}

urlpatterns = [
    path("yonetim/", admin.site.urls),
    path("", v.home, name="home"),
    path("urunler/", v.all_products, name="all_products"),
    path("<slug:slug>-yedek-parca/", v.brand_page, name="brand_page"),
    path("urun/<slug:slug>/", v.product_detail, name="product_detail"),

    # ✅ robots.txt
    path(
        "robots.txt",
        lambda request: HttpResponse(
            "User-agent: *\n"
            "Allow: /\n"
            "Sitemap: " + settings.SITE_URL.rstrip("/") + "/sitemap.xml\n",
            content_type="text/plain"
        ),
    ),

    # ✅ sitemap.xml
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
