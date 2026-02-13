from django.conf import settings

def business_info(request):
    return {
        "BUSINESS_NAME": "Umay Oto Yedek Parça",
        "BUSINESS_ADDRESS": "Darıca, Kocaeli",
        "BUSINESS_PHONE": "+905331432357",
        "BUSINESS_OWNER": "Yahya Yılmaz",
        "BUSINESS_HOURS": "09:00 – 18:00 (Pzt – Cmt)",
        "BUSINESS_WHATSAPP": "905331432357",
        "BUSINESS_INSTAGRAM": "https://www.instagram.com/umay.oto",
        "MAP_EMBED_SRC": "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d317.57589883183346!2d29.393528009666944!3d40.77723920814849!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14cadf8e01a0f4df%3A0x63d522302409b3cf!2sUmay%20Oto%20Yedek%20Par%C3%A7a!5e0!3m2!1str!2str!4v1755636859221!5m2!1str!2str",
        "SITE_URL": settings.SITE_URL,

    }
