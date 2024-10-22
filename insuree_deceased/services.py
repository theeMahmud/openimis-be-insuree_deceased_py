from core.services import BaseService
from core.signals import register_service_signal
from insuree_deceased.models import InsureeDeceased
from insuree_deceased.validation import InsureeDeceasedValidation


class InsureeDeceasedService(BaseService):
    OBJECT_TYPE = InsureeDeceased

    def __init__(self, user, validation_class = InsureeDeceasedValidation):
        super().__init__(user, validation_class)


    @register_service_signal("insuree_deceased.create")
    def create(self, obj_data):
        super().create(obj_data)
