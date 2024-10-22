from django.core.exceptions import ValidationError

from core.validation import BaseModelValidation
from insuree.models import Insuree
from insuree_deceased.apps import InsureeDeceasedConfig
from insuree_deceased.models import InsureeDeceased


class InsureeDeceasedValidation(BaseModelValidation):
    OBJECT_TYPE = InsureeDeceased

    @classmethod
    def validate_create(cls, user, **data):
        if not user.has_perms(InsureeDeceasedConfig.insuree_deceased_create):
            raise ValidationError("insuree_deceased.validation.insuree_deceased_create")
        check_if_insuree_already_deceased(data)

    @classmethod
    def validate_update(cls, user, **data):
        if not user.has_perms(InsureeDeceasedConfig.insuree_deceased_update):
            raise ValidationError("insuree_deceased.validation.insuree_deceased_update")

    @classmethod
    def validate_delete(cls, user, **data):
        if not user.has_perms(InsureeDeceasedConfig.insuree_deceased_update):
            raise ValidationError("insuree_deceased.validation.insuree_deceased_delete")

def check_if_insuree_already_deceased(data):
    incoming_insuree_id = data.get('insuree_id', None)
    if InsureeDeceased.objects.filter(insuree_id=incoming_insuree_id).exists():
        raise ValidationError("insuree_deceased.validation.check_if_insuree_already_deceased")