"""
Management command para criar temas padrão - FASE 2
Cria temas personalizados para restaurantes existentes
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.restaurantes.models import Restaurante
from apps.core.models import TemaRestaurante


class Command(BaseCommand):
    help = 'Cria temas padrão para restaurantes que não possuem tema personalizado'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a recriação dos temas existentes',
        )
        parser.add_argument(
            '--restaurante',
            type=str,
            help='Slug do restaurante específico para criar tema',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 INICIANDO CRIAÇÃO DE TEMAS PADRÃO - FASE 2')
        )

        force = options.get('force', False)
        restaurante_slug = options.get('restaurante')

        # Filtrar restaurantes
        if restaurante_slug:
            restaurantes = Restaurante.objects.filter(slug=restaurante_slug, ativo=True)
            if not restaurantes.exists():
                self.stdout.write(
                    self.style.ERROR(f'❌ Restaurante "{restaurante_slug}" não encontrado')
                )
                return
        else:
            restaurantes = Restaurante.objects.filter(ativo=True)

        temas_criados = 0
        temas_atualizados = 0

        # Paletas de cores predefinidas
        paletas_cores = {
            'pizzaria': {
                'cor_primaria': '#C41E3A',  # Vermelho italiano
                'cor_secundaria': '#2F5233',  # Verde italiano
                'cor_botao': '#FF6B35',  # Laranja vibrante
                'tipo_tema': 'classico'
            },
            'burger': {
                'cor_primaria': '#8B4513',  # Marrom
                'cor_secundaria': '#FFD700',  # Dourado
                'cor_botao': '#FF4500',  # Vermelho-laranja
                'tipo_tema': 'casual'
            },
            'sushi': {
                'cor_primaria': '#1B1B1B',  # Preto elegante
                'cor_secundaria': '#DC143C',  # Vermelho vibrante
                'cor_botao': '#00CED1',  # Turquesa
                'tipo_tema': 'elegante'
            },
            'padaria': {
                'cor_primaria': '#8B4513',  # Marrom pão
                'cor_secundaria': '#F5DEB3',  # Bege
                'cor_botao': '#228B22',  # Verde natural
                'tipo_tema': 'classico'
            },
            'default': {
                'cor_primaria': '#007bff',  # Azul moderno
                'cor_secundaria': '#6c757d',  # Cinza
                'cor_botao': '#28a745',  # Verde
                'tipo_tema': 'moderno'
            }
        }

        with transaction.atomic():
            for restaurante in restaurantes:
                # Verifica se já tem tema
                tema_existente = hasattr(restaurante, 'tema') and restaurante.tema
                
                if tema_existente and not force:
                    self.stdout.write(
                        f'⏭️  {restaurante.nome} já possui tema personalizado'
                    )
                    continue

                # Determina a paleta baseada no nome/tipo do restaurante
                nome_lower = restaurante.nome.lower()
                paleta_escolhida = paletas_cores['default']
                
                if any(word in nome_lower for word in ['pizza', 'pizzaria']):
                    paleta_escolhida = paletas_cores['pizzaria']
                elif any(word in nome_lower for word in ['burger', 'hamburguer', 'lanches']):
                    paleta_escolhida = paletas_cores['burger']
                elif any(word in nome_lower for word in ['sushi', 'japonês', 'oriental']):
                    paleta_escolhida = paletas_cores['sushi']
                elif any(word in nome_lower for word in ['padaria', 'pão', 'café']):
                    paleta_escolhida = paletas_cores['padaria']

                # Cria ou atualiza o tema
                tema_data = {
                    'tipo_tema': paleta_escolhida['tipo_tema'],
                    'nome_personalizado': f'Tema {restaurante.nome}',
                    'cor_primaria': paleta_escolhida['cor_primaria'],
                    'cor_secundaria': paleta_escolhida['cor_secundaria'],
                    'cor_fundo': '#ffffff',
                    'cor_texto': '#212529',
                    'cor_botao': paleta_escolhida['cor_botao'],
                    'fonte_primaria': 'Roboto, sans-serif',
                    'fonte_secundaria': 'Poppins, sans-serif',
                    'tamanho_fonte_base': 16,
                    'largura_maxima': 1200,
                    'espacamento_geral': 15,
                    'border_radius': 8,
                    'ativo': True
                }

                if tema_existente and force:
                    # Atualiza tema existente
                    for key, value in tema_data.items():
                        setattr(restaurante.tema, key, value)
                    restaurante.tema.save()
                    temas_atualizados += 1
                    self.stdout.write(
                        self.style.WARNING(f'🔄 Tema atualizado: {restaurante.nome}')
                    )
                else:
                    # Cria novo tema
                    TemaRestaurante.objects.create(
                        restaurante=restaurante,
                        **tema_data
                    )
                    temas_criados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Tema criado: {restaurante.nome} ({paleta_escolhida["tipo_tema"]})')
                    )

        # Relatório final
        self.stdout.write(
            self.style.SUCCESS(f'\n🎨 TEMAS CRIADOS COM SUCESSO!')
        )
        self.stdout.write(f'   📊 Temas criados: {temas_criados}')
        self.stdout.write(f'   🔄 Temas atualizados: {temas_atualizados}')
        self.stdout.write(f'   📈 Total processado: {temas_criados + temas_atualizados}')
        
        if temas_criados > 0 or temas_atualizados > 0:
            self.stdout.write(
                self.style.SUCCESS('\n🚀 FASE 2 - TEMPLATES WHITE LABEL IMPLEMENTADA!')
            )
            self.stdout.write('   ✅ Cada restaurante agora tem seu tema personalizado')
            self.stdout.write('   ✅ Cores adaptadas ao tipo de negócio')
            self.stdout.write('   ✅ Templates responsivos e modernos')
            self.stdout.write('   ✅ Sistema de cache para performance')
