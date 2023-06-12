from django.core.management.base import BaseCommand
from lojinha.models import CommissionByDay

class Command(BaseCommand):
    """
    Comando para preencher a tabela CommissionByDay com dados padrão.
    """
    help = 'Popula a tabela CommissionByDay com dados padrão.'

    def handle(self, *args, **kwargs):
        commissions = [
            {'day': 0, 'min_commission': 2.0, 'max_commission': 7.0},  # Segunda-feira
            {'day': 1, 'min_commission': 3.0, 'max_commission': 4.0},  # Terça-feira
            {'day': 2, 'min_commission': 1.0, 'max_commission': 5.0},  # Quarta-feira
            {'day': 3, 'min_commission': 5.0, 'max_commission': 8.0},  # Quinta-feira
            {'day': 4, 'min_commission': 8.0, 'max_commission': 10.0}, # Sexta-feira
            {'day': 5, 'min_commission': 5.0, 'max_commission': 9.0},  # Sábado
            {'day': 6, 'min_commission': 3.0, 'max_commission': 6.0},  # Domingo
        ]

        for commission in commissions:
            try:
                CommissionByDay.objects.update_or_create(
                    day_of_week=int(commission['day']),
                    defaults={
                        'min_commission': float(commission['min_commission']),
                        'max_commission': float(commission['max_commission'])
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'''
                                                    CommissionByDay para o dia {commission["day"]} 
                                                    importado com sucesso'''
                                                    )
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'''
                                                   Erro ao importar CommissionByDay para o dia 
                                                   {commission["day"]}: {e} '''
                                                   )
                )
                                                   
