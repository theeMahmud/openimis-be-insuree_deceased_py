from insuree.reports import insuree_family_overview


def insuree_deceased_query(user, date_from=None, date_to=None, **kwargs):
    from django.db.models import Q, F
    from insuree.models import Insuree
    from core import datetimedelta

    queryset = Insuree.objects
    queryset = queryset.filter(Q(deceased__isnull=False))

    if date_from:
        queryset = queryset.filter(Q(deceased__date_created__gte=date_from))

    if date_to:
        queryset = queryset.filter(Q(deceased__date_created__lte=date_to+datetimedelta(days=1)))

    queryset = (
        queryset
        .values(
            "chf_id",
            "other_names",
            "last_name",
            deceased_date=F("deceased__decease_date"),
            village=F("family__location__name"),
            ward=F("family__location__parent__name"),
            district=F("family__location__parent__parent__name"),
        )
        .order_by("district", "ward", "village", "chf_id")
    )

    return {"data": list(queryset)}



report_definitions = [
    {
        "name": "deceased_insurees_report",
        "engine": 0,
        "default_report": insuree_family_overview.template,
        "description": "Insuree deceased",
        "module": "insuree_deceased",
        "python_query": insuree_deceased_query,
        "permission": ["101101"],
    }
]