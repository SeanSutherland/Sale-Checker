from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
import re
from PIL import Image


class Item(models.Model):
    item_name = models.CharField(max_length=200)
    urls = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    regular_price = models.DecimalField(
        decimal_places=2, max_digits=8)
    last_price = models.DecimalField(
        decimal_places=2, max_digits=8, default=Decimal('0.00'))

    on_sale = models.BooleanField(default=False)
    last_url = models.CharField(max_length=1000, blank=True)
    last_site = models.CharField(max_length=200, blank=True)

    image = models.ImageField(
        default='default.jpg', upload_to='item_pics')

    def save(self, *args, **kwargs):
        if self.last_price == 0:
            self.last_price = self.regular_price
        super(Item, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def getSite(self, url):
        try:
            site = re.findall('(\..*\.com|\..*\.ca)', url)
            if len(site) == 0:
                site = re.findall('\/.*\.com', url)
                site = site[0][2:]
            else:
                site = site[0][1:]
            print(site)
            return site
        except:
            return ""

    def getURLs(self):
        list = []
        urls = self.urls.split(",")
        for url in urls:
            a = [url, self.getSite(url)]
            list.append(a)

        return list

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})
