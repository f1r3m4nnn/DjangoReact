from django.db import models

from django.db.models import Max
from django.db import transaction
from django.core.validators import RegexValidator
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)

from utils.model_abstracts import Model, ModelIDInt



phone_regex = r'^\d{10}$|^\d{11}$'
phone_validator = RegexValidator(
    phone_regex,
    "O número de telefone deve estar no formato: 'XXXXXXXXXX' ou 'XXXXXXXXXXX'",
    'invalido'
)



class Customer(TimeStampedModel, Model):
    """
    Customer
    Clqsse/Model para cliente.
    """
    image = models.ImageField(upload_to='customers/', default='customers/default.jpg')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, validators=[phone_validator])
    email = models.EmailField(max_length=255, unique=True)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'



class Seller(TimeStampedModel, Model):
    """
    Seller
    Classe/Model para vendedor.
    """
    image = models.ImageField(upload_to='sellers/', default='sellers/default.jpg')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, validators=[phone_validator])
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'


    def calcCommission(self):
        commission = 0.0
        for order in self.order_set.all():
            for detail in order.details.all():
                commission_day = CommissionByDay.objects.get(day_of_week=order.created.weekday())
                item_commission_rate = detail.item.commission_rate / 100.0
                adjusted_rate = max(item_commission_rate, commission_day.min_commission)
                commission_rate = min(adjusted_rate, commission_day.max_commission)
                commission += commission_rate * detail.item.price * detail.quantity
        return commission



class CommissionByDay(ModelIDInt):
    '''
    CommissionByDay
    Classe/Model para comissão por dia da semana.
    
    A comissão é calculada da seguinte forma:
    1. Se a comissão do item for maior que a comissão mínima do dia, então a comissão do item é usada.
    2. Se a comissão do item for menor que a comissão mínima do dia, então a comissão mínima do dia é usada.
    3. Se a comissão do item for maior que a comissão máxima do dia, então a comissão máxima do dia é usada.
    4. Se a comissão do item for menor que a comissão máxima do dia, então a comissão do item é usada.
    '''
    DAYS_OF_WEEK = (
        (0, 'Segunda'),
        (1, 'Terça'),
        (2, 'Quarta'),
        (3, 'Quinta'),
        (4, 'Sexta'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    )


    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    min_commission = models.FloatField()
    max_commission = models.FloatField()


    class Meta:
        unique_together = ('day_of_week',)



class Item( TimeStampedModel,
            ActivatorModel,
            TitleSlugDescriptionModel,
            Model):

    """
    lojinha.Item
    Classe/Model para item.
    """
    stock = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='products/', default='products/default.jpg')
    commission_rate = models.FloatField(default=0.0)
    cod_prod = models.CharField(max_length=6, blank=True, null=True, unique=True)


    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ["id"]


    def __str__(self):
        return self.title


    def manageStock(self, qty):
        with transaction.atomic():
            # Recarrega o objeto bloqueando-o.
            item = Item.objects.select_for_update().get(id=self.id)
            if item.stock < qty:
                raise ValueError('Não há estoque suficiente para satisfazer a quantidade requerida.')
            item.stock -= qty
            item.save()


    def checkStock(self, qty):
        with transaction.atomic():
            item = Item.objects.select_for_update().get(id=self.id)
            return item.stock >= qty


    def placeOrder(self, user, qty):
        if self.checkStock(qty):
            order = Order.objects.create(
                item = self, 
                quantity = qty, 
                user= user)
            self.manage_stock(qty)
            return order
        else:
            return None


    def save(self, *args, **kwargs):
        """
        Método para salvar um Item no bd. Também se encarrega de gerar/validar o código doproduto (cod_prod).

        Documentação maior, pois é possível que não lembre o que exatamente queria ou pretendia fazer por aqui.

        Passos que este método realiza:
        1. Se o código do produto não for fornecido, este método irá gerar um novo. Faz isso pegando o último item do
        banco de dados que tem um código de produto, tratando as devidas converções de tipos e incrementando esse
        código em 1. Se não houver nenhum item com um código de produto, configura o código do produto como '000001'.

        2. Se um código do produto for fornecido, este método irá primeiro verificar se o código é uma string numérica
        de seis dígitos. Se não for, ele levanta um ValueError. Detalhe para o uso de zfill(6) para preencher com zeros

        3. Em seguida, verifica se o código do produto já está em uso. Para garantir a unicidade do código do produto,
        exclui o item atual da consulta, pois, caso contrário, ele encontrará o próprio código do produto no objeto e
        acreditará incorretamente que o código já está em uso. Se o código já estiver, eevanta um ValueError.

        Finalmente, chama o método save da superclasse para salvar o item no banco de dados.

        Se houver algum problema durante o processo, como um código de produto inválido ou um código de produto já em
        uso, o método levantará um ValueError e imprimirá a mensagem de erro.
        
        """
        initcod_srt = '000001'
        errormessage_invalid_code = 'Código do produto inválido. Deve ser um número de seis dígitos.'
        errormessage_duplicate_code = 'Este código de produto já está em uso. Por favor, escolha um diferente.'
        errormessage_save_failed = 'Um erro ocorreu enquanto a aplicação salvava o item: {error}.'

        try:
            if not self.cod_prod:
                last_item = Item.objects.filter(cod_prod__isnull=False).order_by('-created').first()
                if last_item and last_item.cod_prod.isdigit():
                    self.cod_prod = str(int(last_item.cod_prod) + 1).zfill(6)
                else:
                    self.cod_prod = initcod_srt
            else:
                if not self.cod_prod.isdigit() or len(self.cod_prod) != 6:
                    raise ValueError(errormessage_invalid_code)
                if Item.objects.exclude(id=self.id).filter(cod_prod=self.cod_prod).exists():
                    raise ValueError(errormessage_duplicate_code)
            super().save(*args, **kwargs)
        except ValueError as e:
            print(errormessage_save_failed.format(error=e))
                  


class Order(TimeStampedModel, Model):
    invoice_number = models.IntegerField(unique=True, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    document_date = models.DateField(null=False, blank=False)


    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ["id"]


    def __str__(self):
        return f'{self.invoice_number} - {self.customer.name}'


    def save(self, *args, **kwargs):
        if self.invoice_number is None: # Se o número da fatura não for fornecido, gera um novo.
            max_invoice_number = Order.objects.all().aggregate(Max('invoice_number'))['invoice_number__max'] or 0
            self.invoice_number = max_invoice_number + 1
        super().save(*args, **kwargs)
    


class OrderDetail(Model):
    print('OrderDetail')
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price_at_sale = models.FloatField(blank=True)
    discount = models.FloatField(default=0.0)
    tax = models.FloatField(default=6.0)  # imposto padrão de 6%
    commission = models.FloatField(default=0.0)


    class Meta:
        verbose_name = 'Detalhe da Venda'
        verbose_name_plural = 'Detalhes das Vendas'


    def __str__(self):
        return f'{self.order.invoice_number} - {self.item.title}'


    def save(self, *args, **kwargs):
        """
        Serve basicamente para determinar qual a taxa de comissão a ser aplicada
        baseado no dia da semana contra a comissão individual do item.

        Por exemplo, se o item tem uma comissão de 10% e o dia da semana é segunda-feira,
        com uma comissão mínima de 3% e comissão máxima de 7%, então a comissão a ser
        aplicada será de 7%.

 
        """
        print('OrderDetail.presave()') #Trace
        if True:
            self.price_at_sale = self.item.price
            day_of_week = self.order.document_date.weekday()

            print(f'OrderDetail.save(): day_of_week={day_of_week},{type(day_of_week)}')
            commission_by_day = CommissionByDay.objects.get(day_of_week=day_of_week)
            print(f'OrderDetail.save(): commission_by_day={commission_by_day}')

            if self.item.commission_rate < commission_by_day.min_commission:
                self.commission = commission_by_day.min_commission
            elif self.item.commission_rate > commission_by_day.max_commission:
                self.commission = commission_by_day.max_commission
            else:
                self.commission = self.item.commission_rate
        super().save(*args, **kwargs)

