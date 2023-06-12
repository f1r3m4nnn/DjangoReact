import logging
import random
from datetime import datetime, timedelta

import numpy as np

from django.core.management.base import BaseCommand

from lojinha.models import Customer, Item, Seller
from lojinha.services import OrderService


START_DATE = '2023-05-10'
END_DATE = '2023-06-10'
TOTAL_ORDERS = 180



# Listas de quantidades baseadas em diferentes faixas de preço
quantity_lists = {
    'very_cheap': [10, 12, 20, 24, 30, 40, 48, 50, 60],
    'cheap': [3, 5, 6, 9, 12, 16, 20, 24, 28],
    'affordable': [2, 3, 4, 6, 7, 8, 10, 12, 14, 16],
    'moderate': [2, 3, 4, 5, 6, 7, 8],
    'intermediate': [1, 2, 4, 5],
    'expensive': [1, 2, 3, 4],
    'very_expensive': [1, 2, 3],
    'most_expensive': [1, 2]
}



def setupLogging():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'./logs/logfile_{timestamp}.txt'

    logger = logging.getLogger(__name__)

    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger



def addGames2ORDER(order, pnum, logger):
    all_games = list(Item.objects.filter(title__icontains='jogo:'))

    if len(all_games) >= pnum:
        games = random.sample(all_games, pnum)

        for game in games:
            order_detail = OrderService.createOrderDetail(order=order, item=game, quantity=1)
            order_detail.save()

            logger.info(f'Adicionado jogo {game.title} ao pedido {order.invoice_number}')
    else:
        logger.warning('Não há jogos suficientes em estoque para adicionar ao pedido.')	



def addSketchebook2ORDER(order, pnum, logger):
    all_sketchbooks = list(Item.objects.filter(title__icontains='caderno de desenho')) 

    if len(all_sketchbooks) >= pnum:
        sketchbooks = random.sample(all_sketchbooks, pnum)  # escolhe 2 sketchbooks sem remoção

        for sketchbook in sketchbooks:
            order_detail = OrderService.createOrderDetail(order=order, item=sketchbook, quantity=1)
            order_detail.save()

            logger.info(f'Adicionado caderno de desenho {sketchbook.title} ao pedido {order.invoice_number}')
    else:
        logger.warning('Não há cadernos de desenho suficientes em estoque para adicionar ao pedido.')



def determineQuantity(item):
    title_lower = item.title.lower()
    description_lower = item.description.lower()

    if ('notebook' in title_lower or 'notebook' in description_lower) and item.price > 1300:
        return random.choice(quantity_lists['most_expensive'])
    elif 'caneta' in title_lower and item.price < 5:
        return random.choice(quantity_lists['very_cheap'])
    elif 'caneta' in title_lower and 5 <= item.price < 100:
        return random.choice(quantity_lists['cheap'])
    elif 'caneta' in title_lower and item.price >= 100:
        return random.choice(quantity_lists['most_expensive'])
    elif title_lower.startswith('jogo:') or title_lower.startswith('placa de vídeo') or title_lower.startswith('videogame'):  # noqa: E501
        return 1
    elif title_lower.startswith('teclado'):
        return random.choice(quantity_lists['expensive'])
    elif ('celular' in title_lower or 'celular' in description_lower) and item.price > 698:
        return 1
    elif 0.01 <= item.price < 6:
        return random.choice(quantity_lists['very_cheap'])
    elif 6 <= item.price < 20:
        return random.choice(quantity_lists['cheap'])
    elif 20 <= item.price < 50:
        return random.choice(quantity_lists['affordable'])
    elif 50 <= item.price < 120:
        return random.choice(quantity_lists['moderate'])
    elif 120 <= item.price < 250:
        return random.choice(quantity_lists['intermediate'])
    elif 250 <= item.price < 750:
        return random.choice(quantity_lists['expensive'])
    elif 750 <= item.price < 1300:
        return random.choice(quantity_lists['very_expensive'])
    else:
        return random.choice(quantity_lists['most_expensive'])
    


def printOrderSummary(orders, logger):
    logger.info('Printando resumo dos pedidos:')
    total_orders = 0
    for order_date in orders:
        logger.info(f'Data: {order_date["date"]}, Total de Pedidos: {order_date["num_orders"]}')
        total_orders += order_date['num_orders']
    logger.info(f'Total de pedidos distribuídos: {total_orders}')



def distributeOrders(total_orders, start_date, end_date, logger, max_iterations=200000):
    logger.info(f'Inciando distribuição. Total de pedidos: {total_orders}')
    delta_date = end_date - start_date
    date_weights = [0]*7  # Inicializa lista de pesos para cada dia da semana
    date_weights[0] = 2  # Setando peso maior para segunda-feira
    date_weights[1] = 2  # Setando peso maior para terça-feira
    date_weights[2:] = [0.8, 0.6, 0.4, 0.45, 0.62]  # Setando pesos para os demais dias da semana
    orders = []

    # Distribuíndo pedidos entre as datas.
    for i in range(delta_date.days + 1):
        date = start_date + timedelta(days=i)
        if date.weekday() < 6:  # Exclui domingos.
            orders.append({
                'date': date,
                'weight': date_weights[date.weekday()],
                'num_orders': 0
            })

    remaining_orders = total_orders
    logger.info(f'Pedidos restantes: {remaining_orders}')

    iteration = 0
    while remaining_orders > 0 and iteration <= max_iterations:
        logger.info(f'Iterando: {iteration+1}')

        # Calculando o peso total
        total_weight = sum(order_date['weight'] for order_date in orders)

        # Escolhendo uma data aleatória baseado no peso
        r = random.uniform(0, total_weight)
        cumulative_weight = 0
        for order_date in orders:
            cumulative_weight += order_date['weight']
            if r <= cumulative_weight:
                break

        num_orders = 1  # Inicializa o número de pedidos para a data escolhida

        order_date['num_orders'] += num_orders
        remaining_orders -= num_orders
        logger.info(
            f'Pedido adicionado. Data: {order_date["date"]}, '
            f'Total de pedidos para essa data: {order_date["num_orders"]}, Restantes: {remaining_orders}'
        )

        # Atualizando o peso da pedido em função dos remancescentes
        order_date['weight'] = remaining_orders / total_orders * date_weights[order_date['date'].weekday()]

        iteration += 1

    if iteration > max_iterations:
        logger.warning('Número máximo de iterações atingido. A distribuição não foi concluída.')

    logger.info(f'Distribuição concluída em {iteration} iterações. Pedidos restantes: {remaining_orders}')

    # Resumo
    printOrderSummary(orders, logger)

    return orders


    

def simulateOrder(total_orders, start_date, end_date, logger):
    successful_orders = 0
    attempts = 0
    max_attempts = total_orders * 10

    orders = distributeOrders(total_orders, start_date, end_date, logger)

    all_customers = list(Customer.objects.all())
    all_sellers = list(Seller.objects.all())
    all_items = list(Item.objects.all())

    for order_date in orders:
        for _ in range(order_date['num_orders']):
            try:
                order = None
                customer = random.choice(all_customers)
                seller = random.choice(all_sellers)

                num_unique_items = random.randint(1, 7)

                order = OrderService.createOrder(customer=customer, seller=seller, document_date=order_date['date'])
                all_order_details = []

                for _ in range(num_unique_items):
                    item = random.choice(all_items)

                    if any(detail.item == item for detail in all_order_details):
                        continue

                    quantity = determineQuantity(item)

                    ###################################################
                    # Simula o desconto de 5% a 10% em 10% dos details
                    random_number = random.randint(1, 10)

                    if random_number == 10:
                        discount = random.uniform(5, 10)
                    else:
                        discount = 0.0
                    #
                    ###################################################

                    order_detail = OrderService.createOrderDetail(order=order,
                                                                  item=item,
                                                                  quantity=quantity,
                                                                  discount=discount
                    )
                    all_order_details.append(order_detail)

                    title_lower = item.title.lower()
                    description_lower = item.description.lower()

                    if 'cadeira gamer' in title_lower or 'cadeira gamer' in description_lower:
                        addGames2ORDER(order, 2, logger)

                    if 'placa de vídeo' in title_lower or 'placa de vídeo' in description_lower:
                        addGames2ORDER(order, 1, logger)

                    if 'pc gamer' in title_lower or 'pc gamer' in description_lower:
                        addGames2ORDER(order, 5, logger)

                    if 'lápis' in title_lower and 'faber castell' in title_lower:
                        addSketchebook2ORDER(order, 1, logger)

                    if 'cabo de rede' in title_lower and  quantity > 2:
                        quantity = random.randint(1, 2)

                    if 'cabo usb' in title_lower and  quantity > 2:
                        quantity = random.randint(1, 2)
                    
                    if 'cabo hdmi' in title_lower and  quantity > 2:
                        quantity = random.randint(1, 2)
                    
                    if 'microsoft 365 family' in title_lower and  quantity > 1:
                        quantity = 1

                    if (('impressora' in title_lower or 'impressora' in description_lower) or
                        ('multifuncional' in title_lower or 'multifuncional' in description_lower)) and  quantity > 2:
                        quantity = random.randint(1, 2)
                    

                if all_order_details:
                    order.save()
                    successful_orders += 1
                    logger.info(f"Pedido {order.invoice_number} criado com sucesso")

            except IndexError as ie:
                logger.error(f"Erro criando o pedido: não há itens suficientes. Detalhes: {str(ie)}")
            except Exception as e:
                if order is not None:
                    logger.error(f"Erro criando o pedido {order.invoice_number}: {str(e)}")
                else:
                    logger.error(f"Erro criando pedido: {str(e)}")
            finally:
                attempts += 1

            if attempts >= max_attempts:
                error_message = f"Número máximo de tentativas ({max_attempts}) atingido. Abortando."
                logger.error(error_message)
                raise Exception(error_message)

    logger.info(f"Foram criados {successful_orders} pedidos com sucesso.")



class Command(BaseCommand):
    help = 'Simula operações de compras/pedidos.'

    def add_arguments(self, parser):
        parser.add_argument('--start_date', type=str, default=START_DATE)
        parser.add_argument('--end_date', type=str, default=END_DATE)
        parser.add_argument('--total_orders', type=int, default=TOTAL_ORDERS)

    def handle(self, *args, **options):
        start_date = options['start_date']
        end_date = options['end_date']
        total_orders = options['total_orders']

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        logger = setupLogging()

        simulateOrder(total_orders, start_date, end_date, logger)