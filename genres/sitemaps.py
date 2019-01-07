from django.contrib.sitemaps import Sitemap
from genres.models import GenreNew


class GenreNewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return GenreNew.objects.all()

    def lastmod(self, obj):
        return obj.date_update