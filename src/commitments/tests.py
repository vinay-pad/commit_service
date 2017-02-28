from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
import json
import unittest
from users.models import User
from rest_framework.test import APIClient


class CommitmentTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.server = 'http://ec2-54-67-126-154.us-west-1.compute.amazonaws.com:8000/'
        self.uname = 'vinay'
        self.pword = 'vinay123'
        self.user = User.objects.create_user('vinay','', 'vinay123')

    def login(self):
        response = self.client.get(self.server+'/v1/users/login/?username='+self.uname+'&password='+self.pword)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.content
        self.assertIn('token', content)
        return json.loads(content)['token']

    def create_commitment(self, token):
        self.client.force_authenticate(user=self.user, token=token)
        resp = self.client.post(self.server+'/v1/commitments/', {'message': 'hello'}, 
                                headers={'HTTP_AUTHORIZATION': 'Token '+str(token)})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        content = resp.content
        content_dict = json.loads(content)
        self.assertIn('id', content_dict)
        self.assertIn('user', content_dict)
        self.assertIn('message', content_dict)
        self.assertIn('created_ts', content_dict)
        self.assertEqual(content_dict['message'], 'hello')

    ### Flow 1 - verify secrecy of message
    def test_case1(self):
        """
        1. User login and gets token.
        2. User creates a commitment.
        3. Verify commitment is accessible via the commit-id
        4. Verify commitment's message is not visible in the GET /v1/commitments/<id>/ endpoint.
        """
        token = self.login()
        commitment_id = self.create_commitment(token)
