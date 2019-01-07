from django.contrib.sitemaps import Sitemap
from books.models import Book


class BooksSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Book.objects.all()

    def lastmod(self, obj):
        return obj.date_update