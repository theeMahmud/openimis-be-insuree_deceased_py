import graphene

from django.db import transaction

from core.gql.gql_mutations.base_mutation import BaseHistoryModelCreateMutationMixin, BaseMutation
from core.schema import OpenIMISMutation
from insuree_deceased.models import InsureeDeceased
from insuree_deceased.services import InsureeDeceasedService
from insuree_deceased.validation import InsureeDeceasedValidation


class CreateInsureeDeceasedInputType(OpenIMISMutation.Input):
    insuree_id = graphene.Int(required=True)
    decease_date = graphene.DateTime(required=True)

class UpdateInsureeDeceasedInputType(CreateInsureeDeceasedInputType):
    id = graphene.Int(required=True)

class CreateInsureeDeceasedMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "CreateInsureeDeceasedMutation"
    _mutation_module = "insuree_deceased"
    _model = InsureeDeceased

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        InsureeDeceasedValidation.validate_create(user, **data)

    @classmethod
    def _mutate(cls, user, **data):
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        service = InsureeDeceasedService(user)
        result = service.create(data)
        return result

    class Input(CreateInsureeDeceasedInputType):
        pass

class UpdateInsureeDeceasedMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "UpdateInsureeDeceasedMutation"
    _mutation_module = "insuree_deceased"
    _model = InsureeDeceased

    @classmethod
    def _mutate(cls, user, **data):
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        service = InsureeDeceasedService(user)
        result = service.update(data)

        return result

    class Input(UpdateInsureeDeceasedInputType):
        pass



class DeleteInsureeDeceasedMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "UpdateInsureeDeceasedMutation"
    _mutation_module = "insuree_deceased"
    _model = InsureeDeceased

    @classmethod
    def _mutate(cls, user, **data):
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        ids = data.get('ids')
        if not ids:
            return {'success': False, 'message': 'No IDs to delete', 'details': ''}

        service = InsureeDeceasedService(user)
        with transaction.atomic():
            for obj_id in ids:
                res = service.delete({'id': obj_id, 'user': user})
                if not res['success']:
                    transaction.rollback()
                    return res

    class Input:
        ids = graphene.List(graphene.NonNull(graphene.String))


