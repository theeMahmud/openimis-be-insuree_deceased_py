from django.db import models

from core.models import HistoryModel


# Create your models here.

class InsureeDeceased(HistoryModel):
    decease_date = models.DateField()
    insuree = models.ForeignKey("Insuree", on_delete=models.DO_NOTHING,
                                db_column='InsureeID', blank=True, null=True)