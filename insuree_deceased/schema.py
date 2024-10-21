import graphene
import graphene_django_optimizer as gql_optimizer

from core.schema import OrderedDjangoFilterConnectionField
from insuree_deceased.gql_mutations import CreateInsureeDeceasedMutation, UpdateInsureeDeceasedMutation, \
    DeleteInsureeDeceasedMutation
from insuree_deceased.gql_queries import InsureeDeceasedGQLType

from insuree_deceased.models import InsureeDeceased
from insuree_deceased.validation import InsureeDeceasedValidator


class Query(graphene.ObjectType):
    insuree_deceased = OrderedDjangoFilterConnectionField(
        InsureeDeceasedGQLType,
        orderBy=graphene.List(of_type=graphene.String)
    )

    def resolve_insuree_deceased(self, info, **kwargs):
        InsureeDeceasedValidator.validate_query(info.context.user)
        if not kwargs.get('insuree__uuid'):
            raise ValueError('Insuree UUID has to be provide to get deceased data')
        query = InsureeDeceased.objects.filter(**kwargs)
        return gql_optimizer.query(query, info)


class Mutation(graphene.ObjectType):
    create_deceased_insuree = CreateInsureeDeceasedMutation.Field()
    update_deceased_insuree = UpdateInsureeDeceasedMutation.Field()
    delete_deceased_insuree = DeleteInsureeDeceasedMutation.Field()

# reminder that we could use signals, but we are not using them during the practice
# def bind_signals():
#     signal_mutation_module_validate[MODULE_NAME].connect(define_what_should_happen_on_mutation_validation)
