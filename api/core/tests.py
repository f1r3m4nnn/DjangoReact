from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from . models import Contact



class ContactTestCase(APITestCase):

    """
    Suite de testes para o ContactViewSet
    """
    def setUp(self):
        self.client = APIClient()
        self.data = {
            'name': 'Patolino',
            'message': 'Mensagem teste.',
            'email': 'patolino@routerlabs.io'
        }
        self.url = '/contact/'

    def test_create_contact(self):
        '''
        Teste para o método create do ContactViewSet.
        '''
        data = self.data
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().title, 'Patolino')


    def test_create_contact_without_name(self):
        '''
        Teste para o método create do ContactViewSet quando name não está nos dados.
        '''
        data = self.data
        data.pop("name")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_create_contact_when_name_equals_blank(self):
        '''
       Teste para o método create do ContactViewSet quando name está em branco.
        '''
        data = self.data
        data['name'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_contact_without_message(self):
        '''
        Teste para o método create do ContactViewSet quando message não está nos dados.
        '''
        data = self.data
        data.pop('message')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_contact_when_message_equals_blank(self):
        '''
        Teste para o método create do ContactViewSet quando message está em branco.
        '''
        data = self.data
        data['message'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_contact_without_email(self):
        '''
        Teste para o método create do ContactViewSet quando email não está nos dados.
        '''
        data = self.data
        data.pop('email')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_contact_when_email_equals_blank(self):
        '''
        Teste para o método create do ContactViewSet quando email está em branco.
        '''
        data = self.data
        data['email'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_contact_when_email_equals_non_email(self):
        '''
        Teste para o método create do ContactViewSet quando email não é um email válido.
        '''
        data = self.data
        data['email'] = 'test'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)