from django.contrib.sitemaps import Sitemap
from collection.models import Collection


class CollectionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Collection.objects.all()

    def lastmod(self, obj):
        return obj.date_update