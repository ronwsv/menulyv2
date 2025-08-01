# Generated by Django 5.2.4 on 2025-07-31 11:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("restaurantes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(max_length=200, verbose_name="Nome Completo"),
                ),
                ("telefone", models.CharField(max_length=20, verbose_name="Telefone")),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="Email"),
                ),
                (
                    "endereco_rua",
                    models.CharField(blank=True, max_length=200, verbose_name="Rua"),
                ),
                (
                    "endereco_numero",
                    models.CharField(blank=True, max_length=20, verbose_name="Número"),
                ),
                (
                    "endereco_complemento",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Complemento"
                    ),
                ),
                (
                    "endereco_bairro",
                    models.CharField(blank=True, max_length=100, verbose_name="Bairro"),
                ),
                (
                    "endereco_cidade",
                    models.CharField(blank=True, max_length=100, verbose_name="Cidade"),
                ),
                (
                    "endereco_estado",
                    models.CharField(blank=True, max_length=2, verbose_name="Estado"),
                ),
                (
                    "endereco_cep",
                    models.CharField(blank=True, max_length=9, verbose_name="CEP"),
                ),
                (
                    "endereco_referencia",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Ponto de Referência"
                    ),
                ),
                (
                    "criado_em",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criado em"),
                ),
            ],
            options={
                "verbose_name": "Cliente",
                "verbose_name_plural": "Clientes",
            },
        ),
        migrations.CreateModel(
            name="Pedido",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "numero",
                    models.CharField(
                        max_length=20, unique=True, verbose_name="Número do Pedido"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("recebido", "Recebido"),
                            ("confirmado", "Confirmado"),
                            ("preparando", "Preparando"),
                            ("pronto", "Pronto"),
                            ("saiu_entrega", "Saiu para Entrega"),
                            ("entregue", "Entregue"),
                            ("cancelado", "Cancelado"),
                        ],
                        default="recebido",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("delivery", "Delivery"),
                            ("retirada", "Retirada no Local"),
                        ],
                        default="delivery",
                        max_length=10,
                        verbose_name="Tipo de Entrega",
                    ),
                ),
                (
                    "endereco_entrega_rua",
                    models.CharField(max_length=200, verbose_name="Rua"),
                ),
                (
                    "endereco_entrega_numero",
                    models.CharField(max_length=20, verbose_name="Número"),
                ),
                (
                    "endereco_entrega_complemento",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Complemento"
                    ),
                ),
                (
                    "endereco_entrega_bairro",
                    models.CharField(max_length=100, verbose_name="Bairro"),
                ),
                (
                    "endereco_entrega_cidade",
                    models.CharField(max_length=100, verbose_name="Cidade"),
                ),
                (
                    "endereco_entrega_estado",
                    models.CharField(max_length=2, verbose_name="Estado"),
                ),
                (
                    "endereco_entrega_cep",
                    models.CharField(max_length=9, verbose_name="CEP"),
                ),
                (
                    "endereco_entrega_referencia",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Ponto de Referência"
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Subtotal"
                    ),
                ),
                (
                    "taxa_entrega",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=6,
                        verbose_name="Taxa de Entrega",
                    ),
                ),
                (
                    "desconto",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=8,
                        verbose_name="Desconto",
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Total"
                    ),
                ),
                (
                    "forma_pagamento",
                    models.CharField(
                        choices=[
                            ("dinheiro", "Dinheiro"),
                            ("cartao_debito", "Cartão de Débito"),
                            ("cartao_credito", "Cartão de Crédito"),
                            ("pix", "PIX"),
                        ],
                        max_length=20,
                        verbose_name="Forma de Pagamento",
                    ),
                ),
                (
                    "troco_para",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=8,
                        null=True,
                        verbose_name="Troco para",
                    ),
                ),
                (
                    "observacoes",
                    models.TextField(blank=True, verbose_name="Observações"),
                ),
                (
                    "criado_em",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criado em"),
                ),
                (
                    "confirmado_em",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Confirmado em"
                    ),
                ),
                (
                    "pronto_em",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Pronto em"
                    ),
                ),
                (
                    "entregue_em",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Entregue em"
                    ),
                ),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pedidos",
                        to="pedidos.cliente",
                        verbose_name="Cliente",
                    ),
                ),
                (
                    "restaurante",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pedidos",
                        to="restaurantes.restaurante",
                        verbose_name="Restaurante",
                    ),
                ),
            ],
            options={
                "verbose_name": "Pedido",
                "verbose_name_plural": "Pedidos",
                "ordering": ["-criado_em"],
            },
        ),
        migrations.CreateModel(
            name="ItemPedido",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantidade", models.PositiveIntegerField(verbose_name="Quantidade")),
                (
                    "preco_unitario",
                    models.DecimalField(
                        decimal_places=2, max_digits=8, verbose_name="Preço Unitário"
                    ),
                ),
                (
                    "opcoes_selecionadas",
                    models.JSONField(
                        blank=True, default=dict, verbose_name="Opções Selecionadas"
                    ),
                ),
                (
                    "observacoes",
                    models.TextField(blank=True, verbose_name="Observações do Item"),
                ),
                (
                    "produto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="restaurantes.produto",
                        verbose_name="Produto",
                    ),
                ),
                (
                    "pedido",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itens",
                        to="pedidos.pedido",
                        verbose_name="Pedido",
                    ),
                ),
            ],
            options={
                "verbose_name": "Item do Pedido",
                "verbose_name_plural": "Itens do Pedido",
            },
        ),
    ]
