from core.service_signals import ServiceSignalBindType
from core.signals import bind_service_signal
from insuree.signals import signal_before_insuree_search_query
from insuree_deceased.models import InsureeDeceased
from insuree_deceased.services import InsureeDeceasedService
from django.db.models import Q

def append_isDeceased_filter_if_available(sender, **kwargs):
    additional_filter = kwargs.get('additional_filter', None)
    if "insureeDeceased" in additional_filter:
        return Q(
            deceased__isnull=not additional_filter['insureeDeceased']
        )
    InsureeDeceased.objects.filter(is_null=True)

signal_before_insuree_search_query.connect(append_isDeceased_filter_if_available)

def bind_service_signals():
    bind_service_signal(
        'insuree_service.create_or_update',
        update_insuree_deceased_information,
        bind_type=ServiceSignalBindType.AFTER
    )

def update_insuree_deceased_information(**kwargs):
    model = kwargs.get('result', None)
    deceased = model.jsonExt.pop('insureeDeceased').get("deceasedDate", None) if model.jsonExt else None
    insuree_deceased = InsureeDeceased.objects.filter(insuree=model).first()
    if not insuree_deceased:
        InsureeDeceasedService(kwargs['sender'].user).create({
            'decease_date': deceased['deceaseDate'],
            'insuree': model
        })
    else:
        InsureeDeceasedService(kwargs['sender'].user).update({
            'decease_date': deceased['deceaseDate'],
            'insuree': model,
            'id': insuree_deceased.id
        })
    model.save()
