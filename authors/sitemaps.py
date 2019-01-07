from django.contrib.sitemaps import Sitemap
from authors.models import Author


class AuthorsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Author.objects.all()

    def lastmod(self, obj):
        return obj.date_update