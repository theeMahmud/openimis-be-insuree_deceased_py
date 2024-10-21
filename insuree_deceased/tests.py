import json

from dataclasses import dataclass

from django.conf import settings
from graphql_jwt.shortcuts import get_token
from rest_framework import status

from core import datetime
from core.models import User, filter_validity

from django.test import TestCase

from core.models.openimis_graphql_test_case import openIMISGraphQLTestCase
from core.test_helpers import create_test_interactive_user
from insuree.test_helpers import create_test_insuree
from insuree_deceased.models import InsureeDeceased

# Create your tests here.

insuree_deceased_query_string = '''
    query(
    $insuree_Uuid:String
    ){
  insureeDeceased(
     insuree_Uuid:$$insuree_Uuid) {
    totalCount
    edges {
      node {
        deceaseDate
      }
    }
  }
}

'''


@dataclass
class DummyContext:
    """ Just because we need a context to generate. """
    user: User


class InsureeDeceasedGQLTestCase(openIMISGraphQLTestCase):
    GRAPHQL_URL = f'/{settings.SITE_ROOT()}graphql'

    GRAPHQL_SCHEMA = True

    admin_user = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user = create_test_interactive_user(username="testLocationAdmin")
        cls.admin_token = get_token(cls.admin_user, DummyContext(user=cls.admin_user))
        cls.test_insuree = create_test_insuree(with_family=True, custom_props={})
        cls.test_decease_date = InsureeDeceased(
            decease_date=datetime.datetime(2023, 3, 17),
            insuree=cls.test_insuree
        )

    def text_insuree_deceased_query(self):
        response = self.query(
            f"{insuree_deceased_query_string}",
            variables={"insuree_Uuid": self.test_insuree.uuid},
            headers={"HTTP_AUTHORIZATION_TOKEN": f"Bearer {self.admin_token}"},
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content)

        self.assertTrue()
