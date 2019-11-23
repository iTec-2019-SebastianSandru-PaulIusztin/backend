from django.contrib.gis.db.models import PointField
from django.db import models

from apps.shop.models.users import Seller


class Store(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='stores')

    name = models.CharField(max_length=64)
    point = PointField()

    @property
    def lat(self):
        return self.point.y

    @property
    def lng(self):
        return self.point.x
