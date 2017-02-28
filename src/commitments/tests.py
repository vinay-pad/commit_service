from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
import json
import unittest
from users.models import User
from rest_framework.test import APIClient
import os

class CommitmentTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.server = os.environ.get('TEST_SERVER')
        self.uname = os.environ.get('TEST_USER')
        self.pword = os.environ.get('TEST_PWD')
        self.user = User.objects.create_user(self.uname,'', self.pword)

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
        return content_dict['id']

    def get_commitment(self, commitment_id):
        resp = self.client.get(self.server+'/v1/commitments/'+str(commitment_id)+'/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        content = resp.content
        content_dict = json.loads(content)
        self.assertIn('id', content_dict)
        self.assertIn('user', content_dict)
        self.assertNotIn('message', content_dict)
        self.assertNotIn('created_ts', content_dict)

    def make_commitment_readable(self, commitment_id, token):
        self.client.force_authenticate(user=self.user, token=token)
        resp = self.client.post(self.server+'/v1/commitments/'+str(commitment_id)+'/readability/',
                                headers={'HTTP_AUTHORIZATION': 'Token '+str(token)})
        return resp

    def commitment_verify(self, commitment_id):
        resp = self.client.get(self.server+'/v1/commitments/'+str(commitment_id)+'/verification/')
        return resp

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
        self.get_commitment(commitment_id)

    ### Flow 2 - verify message can be revealed only once irrevocably.
    def test_case2(self):
        """
        1. Repeat steps 1 to 4 from Flow 1.
        2. POST to the readability endpoint to make the message readable.
        3. Repeat step 2 and verify it doesnt change anything in the resource.
        """
        token = self.login()
        commitment_id = self.create_commitment(token)
        self.get_commitment(commitment_id)
        resp = self.make_commitment_readable(commitment_id, token)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.make_commitment_readable(commitment_id, token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    ### Flow 3 - verify message hasn't been tampered with since creation
    def test_case3(self):
        """
            1. Repeat steps 1 to 4 from Flow 1.
            2. Call the verification endpoint and verify that the 'tampered' flag is false.
        """
        token = self.login()
        commitment_id = self.create_commitment(token)
        self.get_commitment(commitment_id)
        resp = self.commitment_verify(commitment_id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        content = resp.content
        content_dict = json.loads(content)
        self.assertIn('tampered', content_dict)
        self.assertEqual(content_dict['tampered'], False)
