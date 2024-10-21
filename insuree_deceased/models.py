from django.db import models

from core.models import HistoryModel
from datetime import datetime as py_datetime
from insuree.models import Insuree


# Create your models here.

class InsureeDeceased(HistoryModel):
    decease_date = models.DateTimeField(db_column='DateDeceased', default=py_datetime.now)
    insuree = models.ForeignKey(Insuree, on_delete=models.DO_NOTHING, db_column='InsureeID', blank=True, null=True, related_name='deceased')