from django.db import models
from django.utils.text import slugify
from django.urls import reverse


def unique_slugify(instance, value, slug_field_name="slug", max_length=160):
    """
    Aynı slug oluşursa otomatik -2, -3 diye devam eder.
    IntegrityError riskini pratikte sıfıra indirir.
    """
    slug_field = instance._meta.get_field(slug_field_name)
    base_slug = slugify(value)[:max_length] or "item"

    slug = base_slug
    ModelClass = instance.__class__

    # Update işleminde kendi kaydını hariç tut
    qs = ModelClass.objects.all()
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)

    i = 2
    while qs.filter(**{slug_field.attname: slug}).exists():
        suffix = f"-{i}"
        cut = max_length - len(suffix)
        slug = f"{base_slug[:cut]}{suffix}"
        i += 1

    setattr(instance, slug_field.attname, slug)


class Category(models.Model):
    name = models.CharField("Kategori Adı", max_length=80, unique=True)
    slug = models.SlugField("URL Kısaltması", max_length=90, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name, max_length=90)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"


class Brand(models.Model):
    name = models.CharField("Marka Adı", max_length=80, unique=True)
    slug = models.SlugField("URL Kısaltması", max_length=90, unique=True, blank=True)
    logo = models.ImageField("Logo", upload_to="brands/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name, max_length=90)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Markalar"


class Product(models.Model):
    name = models.CharField("Ürün Adı", max_length=140)
    slug = models.SlugField("URL Kısaltması", max_length=160, unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        verbose_name="Kategori",
        on_delete=models.PROTECT,
        related_name="products"
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name="Marka",
        on_delete=models.PROTECT,
        related_name="products"
    )

    oem_code = models.CharField(
        "OEM / Parça Kodu",
        max_length=120,
        db_index=True,
        blank=True
    )
    compatible = models.CharField(
        "Uyumlu Araç(lar)",
        max_length=240,
        blank=True,
        help_text="Örn: Fiat Egea 1.6D 2016-2020"
    )
    short_desc = models.TextField("Kısa Açıklama", blank=True)

    image = models.ImageField(
        "Ürün Görseli",
        upload_to="products/",
        blank=True,
        null=True
    )


    featured = models.BooleanField("Öne Çıkar", default=False, db_index=True)
    created_at = models.DateTimeField("Eklenme Tarihi", auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["oem_code"]),
        ]
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"

    def save(self, *args, **kwargs):
        if not self.slug:
            # OEM boş olsa bile benzersiz slug üretilecek
            base = f"{self.name}-{self.brand.name}-{self.oem_code}".strip("-")
            unique_slugify(self, base, max_length=160)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    def __str__(self):
        return self.name
