from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Product, Brand

def home(request):
    # Sadece ürünü olan markalar
    brands = (Brand.objects
              .annotate(product_count=Count("products"))
              .filter(product_count__gt=0)
              .order_by("name"))
    return render(request, "home.html", {"brands": brands})

def all_products(request):
    q = request.GET.get("q", "").strip()
    qs = Product.objects.select_related("brand", "category").order_by("-created_at")
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(oem_code__icontains=q) |
            Q(compatible__icontains=q) |
            Q(brand__name__icontains=q) |
            Q(category__name__icontains=q)
        )
    return render(request, "products.html", {"products": qs, "q": q})

def brand_page(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = (Product.objects
                .select_related("brand", "category")
                .filter(brand=brand)
                .order_by("-created_at"))
    return render(request, "brand.html", {"brand": brand, "products": products})

def product_detail(request, slug):
    p = get_object_or_404(Product.objects.select_related("brand", "category"), slug=slug)
    return render(request, "product_detail.html", {"p": p})


