from django.core.management.base import BaseCommand
from lojinha.models import Seller

class Command(BaseCommand):
    """
    Comando para criar os sellers, pois ninguém merece digitar essa parada.
    """
    help = 'Popula a tabela de sellers.'

    def handle(self, *args, **kwargs):
        sellers = [
            {'name': 'Pernalonga', 'phone': '3333333333', 'email': 'pernalonga@maestro.com', 'image': 'sellers/pernalonga.jpg'},  # noqa: E501
            {'name': 'Patolino', 'phone': '4444444444', 'email': 'patolino@maiordetodosostempos.com', 'image': 'sellers/patolino.jpg'},  # noqa: E501
            {'name': 'Tweety Bird', 'phone': '5555555555', 'email': 'tweety@bird.com', 'image': 'sellers/tweety.jpg'},
            {'name': 'Sylvester', 'phone': '6666666666', 'email': 'sylvester@cat.com', 'image': 'sellers/sylvester.jpg'},  # noqa: E501
            {'name': 'Speedy Gonzales', 'phone': '7777777777', 'email': 'speedy@gonzalez.com', 'image': 'sellers/speedy.jpg'},  # noqa: E501
            {'name': 'Marvin the Martian', 'phone': '8888888888', 'email': 'marvin@themartian.com', 'image': 'sellers/marvin.jpg'}  # noqa: E501
        ]

        for seller in sellers:
            try:
                Seller.objects.create(name=seller['name'], phone=seller['phone'], email=seller['email'], image=seller['image'])  # noqa: E501
                self.stdout.write(self.style.SUCCESS(f'Seller {seller["name"]} importado com sucesso'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao importar o seller {seller["name"]}: {e}'))

