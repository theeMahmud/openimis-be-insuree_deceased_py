import logging

from core.services import BaseService
from core.signals import register_service_signal
from insuree_deceased.models import InsureeDeceased
from insuree_deceased.validation import InsureeDeceasedValidator

logger = logging.getLogger(__name__)


class DeceasedInsureeService(BaseService):
    OBJECT_TYPE = InsureeDeceased

    def __init__(self, user, validation_class=InsureeDeceasedValidator):
        super().__init__(user, validation_class)

    @register_service_signal('insuree_deceased.create')
    def create(self, obj_data):
        return super().create(obj_data)

    def delete(self, obj_data):
        return super().delete(obj_data)

    def update(self, obj_data):
        return super().update(obj_data)


