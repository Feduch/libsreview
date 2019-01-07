from django.contrib.sitemaps import Sitemap
from publications.models import Publication


class PublicationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Publication.objects.all()

    def lastmod(self, obj):
        return obj.date_update