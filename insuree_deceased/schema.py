import graphene

from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser

from core.schema import OrderedDjangoFilterConnectionField
from insuree_deceased.apps import InsureeDeceasedConfig
from insuree_deceased.gql_mutations import CreateInsureeDeceasedMutation
from insuree_deceased.gql_queries import InsureeDeceaseGQLType
from insuree_deceased.models import InsureeDeceased


class Query(graphene.ObjectType):
    insuree_deceased = OrderedDjangoFilterConnectionField(
        InsureeDeceaseGQLType
    )

    def resolve_insuree_deceased(self, info, **kwargs):
        Query._check_permissions(info.context.user, InsureeDeceasedConfig.insuree_deceased_search)
        if not kwargs.get('insuree__uuid'):
            raise ValueError("Insuree UUID has to be provide to get deceased data")
        return InsureeDeceased.objects.filter(**kwargs)

    @staticmethod
    def _check_permissions(user, perms):
        if type(user) is AnonymousUser or not user.id or not user.has_perms(perms):
            raise PermissionError("Unauthorized")


class Mutation(graphene.ObjectType):
    create_insuree_deceased = CreateInsureeDeceasedMutation.Field()