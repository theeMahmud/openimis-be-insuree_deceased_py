from django.db import models
from core.fields import DateTimeField
from core.models import HistoryModel
from insuree.models import Insuree

from datetime import datetime as py_datetime


class InsureeDeceased(HistoryModel):
    decease_date = DateTimeField(db_column="DateDeceased", default=py_datetime.now)
    insuree = models.ForeignKey(Insuree, models.DO_NOTHING, db_column='InsureeID', blank=True, null=True, related_name="deceased")