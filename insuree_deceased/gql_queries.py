import graphene
from graphene_django import DjangoObjectType

from core import ExtendedConnection, prefix_filterset
from insuree.gql_queries import InsureeGQLType
from insuree_deceased.models import InsureeDeceased



class InsureeDeceaseGQLType(DjangoObjectType):
    class Meta:
        model = InsureeDeceased
        filter_fields = {
            "decease_date": ["exact", "lt", "lte", "gt", "gte", "isnull"],
            **prefix_filterset("insuree__", InsureeGQLType._meta.filter_fields)
        }
        interfaces = (graphene.relay.Node,)
        connection_class = ExtendedConnection