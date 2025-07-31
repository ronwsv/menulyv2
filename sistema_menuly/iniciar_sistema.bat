@echo off
title Sistema Menuly - Delivery Multi-Restaurante
echo.
echo ================================================================
echo                   SISTEMA MENULY - DELIVERY
echo                   Multi-Restaurante White Label
echo ================================================================
echo.
echo Iniciando servidor Django...
echo.
echo URLs Disponiveis:
echo - Home: http://localhost:8000/
echo - Admin Django: http://localhost:8000/admin/
echo - Super Admin: http://localhost:8000/superadmin/
echo - Lista Restaurantes: http://localhost:8000/restaurantes/
echo - Pizzaria do Jose: http://localhost:8000/pizzaria-do-jose/
echo - Burger House: http://localhost:8000/burger-house/
echo.
echo ================================================================
echo                        CREDENCIAIS DE ACESSO
echo ================================================================
echo.
echo SUPER USUARIO (Django Admin):
echo Usuario: admin
echo Senha: admin123
echo URL: http://localhost:8000/admin/
echo.
echo SUPER ADMIN (Painel Administrativo):
echo Usuario: admin
echo Senha: admin123
echo URL: http://localhost:8000/superadmin/
echo.
echo LOJISTA (Dono dos Restaurantes):
echo Usuario: lojista_teste
echo Senha: lojista123
echo URL: http://localhost:8000/lojista/
echo.
echo CLIENTE (Para fazer pedidos):
echo Nao ha cliente pre-cadastrado.
echo Registre-se diretamente no site ou use o checkout como convidado.
echo.
echo ================================================================
echo.
echo Aguarde... Iniciando servidor em http://localhost:8000/
echo Pressione Ctrl+C para parar o servidor
echo.

cd /d "%~dp0"
C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe manage.py runserver

pause
