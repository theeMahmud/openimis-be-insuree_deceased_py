import graphene

from core.schema import OpenIMISMutation
from insuree_deceased.models import InsureeDeceased

from core.gql.gql_mutations.base_mutation import BaseHistoryModelCreateMutationMixin, BaseMutation, \
    BaseHistoryModelDeleteMutationMixin, BaseDeleteMutation, BaseHistoryModelUpdateMutationMixin
from insuree_deceased.services import DeceasedInsureeService
from insuree_deceased.validation import InsureeDeceasedValidator


class InsureeDeceasedInputType(OpenIMISMutation.Input):
    decease_date = graphene.DateTime(required=False)
    json_ext = graphene.String(required=False)
    insuree_id = graphene.Int(required=False, name="insureeId")


class CreateInsureeDeceasedMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "CreateInsureeDeceasedMutation"
    _mutation_module = "insuree_deceased"
    _model = InsureeDeceased

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        InsureeDeceasedValidator.validate_create(user, **data)

    @classmethod
    def _mutate(cls, user, **data):
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        service = DeceasedInsureeService(user)
        result = service.create(data)
        return result

    class Input(InsureeDeceasedInputType):
        pass


class DeleteInsureeDeceasedMutation(BaseHistoryModelDeleteMutationMixin, BaseDeleteMutation):
    _mutation_class = "DeleteInsureeDeceasedMutation"
    _mutation_module = "insuree_deceased"
    _model = InsureeDeceased

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        InsureeDeceasedValidator.validate_delete(user, **data)

    def _mutate(self, user, **data):
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        service = DeceasedInsureeService(user)
        result = service.delete(**data)
        return result

    class Input:
        id = graphene.UUID(required=True)


class InsureeDeceasedUpdateInputType(InsureeDeceasedInputType):
    id = graphene.UUID(required=True)


class UpdateInsureeDeceasedMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "UpdateInsureeDeceasedMutation"
    _mutation_module = "insuree_deceased"
    _model = InsureeDeceased

    @classmethod
    def _validate_mutation(cls, user, **data):
        super()._validate_mutation(user, **data)
        InsureeDeceasedValidator.validate_update(user, **data)

    def _mutate(self, user, **data):
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')

        service = DeceasedInsureeService(user)
        result = service.update(**data)
        return result

    class Input(InsureeDeceasedUpdateInputType):
        pass
