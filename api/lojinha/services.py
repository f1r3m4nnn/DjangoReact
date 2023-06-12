from django.db import transaction
from .models import Order, OrderDetail



class OrderService:

    @staticmethod
    @transaction.atomic
    def createOrderDetail(order, item, quantity, discount=0.0, tax=6.0):
        # Verifica se a quantidade e preço são números não-negativos
        if quantity < 0:
            raise ValueError("Quantidade do pedido deve ser um número não-negativo")
        if item.price < 0:
            raise ValueError("Preço do item deve ser um número não-negativo")

        # Estoque insuficiente
        if not item.checkStock(quantity):
            raise ValueError("Quantidade de estoque insuficiente para este item")

        # Baixa
        item.manageStock(quantity)

        # Cria o Detalhe
        order_detail = OrderDetail.objects.create(
            order=order, 
            item=item, 
            quantity=quantity, 
            price_at_sale=item.price,
            discount=discount,
            tax=tax
        )

        return order_detail



    @staticmethod
    @transaction.atomic
    def deleteOrderDetail(order_detail):
        order_detail.item.stock += order_detail.quantity
        order_detail.item.save()
        order_detail.delete()



    @staticmethod
    @transaction.atomic
    def createOrder(customer, seller, document_date):
        order = Order.objects.create(customer=customer, seller=seller, document_date=document_date)
        return order