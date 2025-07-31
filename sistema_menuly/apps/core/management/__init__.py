"""
Comando para popular o banco de dados com dados de exemplo.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.restaurantes.models import PlanoMensal, Lojista, Restaurante, Categoria, Produto
from decimal import Decimal


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de exemplo...')
        
        # Criar superusuário
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@menuly.com', 'admin123')
            self.stdout.write('✓ Superusuário criado: admin / admin123')
        
        # Criar planos
        plano_basico, created = PlanoMensal.objects.get_or_create(
            nome='Plano Básico',
            defaults={
                'tipo': 'basico',
                'preco_mensal': Decimal('29.90'),
                'max_pedidos_mes': 100,
                'max_produtos': 50,
                'max_restaurantes': 1,
                'tem_impressoras': False,
                'tem_multi_unidades': False,
                'tem_relatorios': False,
                'tem_api': False,
            }
        )
        
        plano_premium, created = PlanoMensal.objects.get_or_create(
            nome='Plano Premium',
            defaults={
                'tipo': 'premium',
                'preco_mensal': Decimal('79.90'),
                'max_pedidos_mes': 500,
                'max_produtos': 200,
                'max_restaurantes': 3,
                'tem_impressoras': True,
                'tem_multi_unidades': True,
                'tem_relatorios': True,
                'tem_api': False,
            }
        )
        
        self.stdout.write('✓ Planos criados')
        
        # Criar usuário lojista
        user_lojista, created = User.objects.get_or_create(
            username='lojista_teste',
            defaults={
                'email': 'lojista@menuly.com',
                'first_name': 'João',
                'last_name': 'Silva'
            }
        )
        if created:
            user_lojista.set_password('lojista123')
            user_lojista.save()
        
        # Criar lojista
        from datetime import date, timedelta
        lojista, created = Lojista.objects.get_or_create(
            user=user_lojista,
            defaults={
                'plano': plano_premium,
                'nome_completo': 'João Silva',
                'cpf': '123.456.789-00',
                'telefone': '(11) 99999-9999',
                'data_vencimento': date.today() + timedelta(days=30),
                'trial_ativo': True,
            }
        )
        
        self.stdout.write('✓ Lojista criado: lojista_teste / lojista123')
        
        # Criar restaurante de exemplo
        restaurante, created = Restaurante.objects.get_or_create(
            slug='pizzaria-do-jose',
            defaults={
                'lojista': lojista,
                'nome': 'Pizzaria do José',
                'cnpj': '12.345.678/0001-90',
                'email': 'contato@pizzariadojose.com',
                'telefone': '(11) 3333-4444',
                'whatsapp': '11999998888',
                'endereco_rua': 'Rua das Pizzas',
                'endereco_numero': '123',
                'endereco_bairro': 'Centro',
                'endereco_cidade': 'São Paulo',
                'endereco_estado': 'SP',
                'endereco_cep': '01234-567',
                'cor_primaria': '#e74c3c',
                'cor_secundaria': '#c0392b',
                'cor_botoes': '#27ae60',
                'slogan': 'As melhores pizzas da cidade!',
                'mensagem_boas_vindas': 'Bem-vindo à nossa pizzaria! Temos as melhores pizzas artesanais da região.',
                'sobre_nos': 'Há mais de 20 anos preparando as melhores pizzas com ingredientes frescos e massa artesanal.',
                'taxa_entrega': Decimal('5.00'),
                'tempo_estimado_entrega': 30,
                'pedido_minimo': Decimal('25.00'),
                'ativo': True,
                'aprovado': True,
                'destaque': True,
            }
        )
        
        self.stdout.write('✓ Restaurante criado: Pizzaria do José')
        
        # Criar categorias
        categoria_pizzas, created = Categoria.objects.get_or_create(
            restaurante=restaurante,
            nome='Pizzas Tradicionais',
            defaults={
                'descricao': 'Nossas pizzas clássicas e mais pedidas',
                'ordem': 1,
            }
        )
        
        categoria_especiais, created = Categoria.objects.get_or_create(
            restaurante=restaurante,
            nome='Pizzas Especiais',
            defaults={
                'descricao': 'Criações exclusivas da casa',
                'ordem': 2,
            }
        )
        
        categoria_bebidas, created = Categoria.objects.get_or_create(
            restaurante=restaurante,
            nome='Bebidas',
            defaults={
                'descricao': 'Bebidas geladas para acompanhar',
                'ordem': 3,
            }
        )
        
        self.stdout.write('✓ Categorias criadas')
        
        # Criar produtos de exemplo
        produtos_exemplo = [
            # Pizzas Tradicionais
            {
                'categoria': categoria_pizzas,
                'nome': 'Pizza Margherita',
                'descricao': 'Molho de tomate, mussarela, manjericão fresco e azeitonas',
                'preco': Decimal('32.90'),
                'destaque': True,
                'calorias': 280,
                'tempo_preparo': 25,
            },
            {
                'categoria': categoria_pizzas,
                'nome': 'Pizza Calabresa',
                'descricao': 'Molho de tomate, mussarela, calabresa e cebola',
                'preco': Decimal('35.90'),
                'destaque': False,
                'calorias': 320,
                'tempo_preparo': 25,
            },
            {
                'categoria': categoria_pizzas,
                'nome': 'Pizza Portuguesa',
                'descricao': 'Molho de tomate, mussarela, presunto, ovos, cebola e azeitonas',
                'preco': Decimal('38.90'),
                'destaque': False,
                'calorias': 350,
                'tempo_preparo': 30,
            },
            
            # Pizzas Especiais
            {
                'categoria': categoria_especiais,
                'nome': 'Pizza do Chef',
                'descricao': 'Molho branco, mussarela, salmão, rúcula e tomate seco',
                'preco': Decimal('45.90'),
                'destaque': True,
                'calorias': 380,
                'tempo_preparo': 35,
            },
            {
                'categoria': categoria_especiais,
                'nome': 'Pizza Vegetariana',
                'descricao': 'Molho de tomate, mussarela, berinjela, abobrinha, pimentão e cebola',
                'preco': Decimal('36.90'),
                'destaque': False,
                'calorias': 250,
                'tempo_preparo': 30,
            },
            
            # Bebidas
            {
                'categoria': categoria_bebidas,
                'nome': 'Coca-Cola 2L',
                'descricao': 'Refrigerante Coca-Cola 2 litros gelado',
                'preco': Decimal('8.90'),
                'destaque': False,
                'calorias': 200,
                'tempo_preparo': 2,
            },
            {
                'categoria': categoria_bebidas,
                'nome': 'Suco de Laranja Natural',
                'descricao': 'Suco natural de laranja 500ml',
                'preco': Decimal('7.50'),
                'destaque': False,
                'calorias': 120,
                'tempo_preparo': 5,
            },
        ]
        
        for produto_data in produtos_exemplo:
            produto, created = Produto.objects.get_or_create(
                restaurante=restaurante,
                nome=produto_data['nome'],
                defaults=produto_data
            )
            if created:
                self.stdout.write(f'  ✓ Produto criado: {produto.nome}')
        
        # Criar segundo restaurante
        restaurante2, created = Restaurante.objects.get_or_create(
            slug='burger-house',
            defaults={
                'lojista': lojista,
                'nome': 'Burger House',
                'email': 'contato@burgerhouse.com',
                'telefone': '(11) 5555-6666',
                'whatsapp': '11988887777',
                'endereco_rua': 'Avenida dos Hambúrgueres',
                'endereco_numero': '456',
                'endereco_bairro': 'Vila Burger',
                'endereco_cidade': 'São Paulo',
                'endereco_estado': 'SP',
                'endereco_cep': '01234-890',
                'cor_primaria': '#f39c12',
                'cor_secundaria': '#e67e22',
                'cor_botoes': '#e74c3c',
                'slogan': 'Hambúrgueres artesanais irresistíveis!',
                'taxa_entrega': Decimal('4.00'),
                'tempo_estimado_entrega': 25,
                'pedido_minimo': Decimal('20.00'),
                'ativo': True,
                'aprovado': True,
                'destaque': True,
            }
        )
        
        if created:
            # Categorias para Burger House
            cat_burgers = Categoria.objects.create(
                restaurante=restaurante2,
                nome='Hambúrgueres',
                descricao='Nossos deliciosos hambúrgueres artesanais',
                ordem=1,
            )
            
            cat_acomp = Categoria.objects.create(
                restaurante=restaurante2,
                nome='Acompanhamentos',
                descricao='Batatas e outros acompanhamentos',
                ordem=2,
            )
            
            # Produtos para Burger House
            Produto.objects.create(
                restaurante=restaurante2,
                categoria=cat_burgers,
                nome='X-Bacon Artesanal',
                descricao='Hambúrguer 180g, bacon, queijo cheddar, alface e tomate',
                preco=Decimal('24.90'),
                destaque=True,
                calorias=650,
                tempo_preparo=20,
            )
            
            Produto.objects.create(
                restaurante=restaurante2,
                categoria=cat_acomp,
                nome='Batata Frita Grande',
                descricao='Porção grande de batata frita sequinha',
                preco=Decimal('12.90'),
                calorias=420,
                tempo_preparo=10,
            )
            
            self.stdout.write('✓ Burger House criado com produtos')
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Sistema populado com sucesso!\n')
        )
        self.stdout.write('📋 Dados criados:')
        self.stdout.write('  • Admin: admin / admin123')
        self.stdout.write('  • Lojista: lojista_teste / lojista123')
        self.stdout.write('  • Restaurantes: Pizzaria do José, Burger House')
        self.stdout.write('  • Mini-sites disponíveis:')
        self.stdout.write('    - http://localhost:8000/pizzaria-do-jose/')
        self.stdout.write('    - http://localhost:8000/burger-house/')
        self.stdout.write('')
        self.stdout.write('🚀 Execute: python manage.py runserver')
        self.stdout.write('📱 Acesse: http://localhost:8000/')
