import json

from django.contrib.auth import get_user_model  # noqa: F401
from django.contrib.auth.models import User  # noqa: F401
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token  # noqa: F401
from rest_framework.test import APIClient 

from lojinha.models import CommissionByDay, Customer, Item, Order, OrderDetail, Seller


class OrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name='Test Customer', phone='1234567890', email='teste@teste.com')
        self.customer2 = Customer.objects.create(name='Test Customer 2', phone='1234567890', email = 'teste@teste2.com')
        self.seller = Seller.objects.create(name='Test Seller', phone='1234567890', email='teste2@teste.com')
        self.item = Item.objects.create(title='Test Item', price=10.00, stock=1000)
        self.order = Order.objects.create(customer=self.customer,
                                          seller=self.seller,
                                          document_date=timezone.now().date(),
                                          invoice_number=1000
        )       

        for day in range(7):
            CommissionByDay.objects.create(day_of_week=day, min_commission=2, max_commission=5)

        self.orderdetail = OrderDetail.objects.create(order=self.order, item=self.item, quantity=2)



    def tearDown(self):
        self.client = None
        self.orderdetail.delete()
        self.order.delete()
        self.customer.delete()
        self.customer2.delete()
        self.seller.delete()
        self.item.delete()
        CommissionByDay.objects.all().delete()  # Para pegar todos os dias criados. O bd de testes é zerado.
        super().tearDown()  # Pega o tearDown da classe pai.



    def test_create_order(self):

        data ={
            "data": {
                "type": "Order",
                "attributes": {
                    "invoice_number": 1200,
                    "document_date": str(timezone.now().date()),
                    "customer": str(self.customer.name),
                    "seller": str(self.seller.name),
                    "details": [
                        {
                            "item_id": str(self.item.id),
                            "quantity": 1
                        }
                    ]
                }
            }
        }
 
        data = json.dumps(data)
        response = self.client.post(reverse('orders'), data,  content_type='application/vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)



    def test_get_order_list(self):
        response = self.client.get(reverse('orders'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_update_order(self):
        self.new_seller = Seller.objects.create(name='Quico')
        self.new_customer = Customer.objects.create(name='Chaves') 
        print(self.order.id, 'order id')
        data = {
            "data": {
                "type": "Order",
                "id": str(self.order.id),
                "attributes": {
                    "invoice_number": 1300,
                    "customer": str(self.new_customer.name),
                    "seller": str(self.new_seller.name),
                    "details": [
                        {
                            "item_id": str(self.item.id),
                            "quantity": 5
                        }
                    ]
                }
            }
        }
        # https://docs.djangoproject.com/en/dev/howto/writing-migrations/#migrations-that-add-unique-fields
        data = json.dumps(data)
        response = self.client.patch(reverse('order-single',
                                             kwargs={'id': self.order.id}),
                                             data,
                                             content_type='application/vnd.api+json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(Order.objects.get(id=self.order.id).customer), (self.new_customer.name))



    def test_delete_order(self):
        response = self.client.delete(reverse('order-single', kwargs={'id': self.order.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)


