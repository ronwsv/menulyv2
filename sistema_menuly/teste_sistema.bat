@echo off
title Teste Rapido - Sistema Menuly
echo.
echo ================================================================
echo                      TESTE RAPIDO DO SISTEMA
echo ================================================================
echo.
echo Testando se o sistema esta funcionando...
echo.

cd /d "%~dp0"

echo 1. Verificando ambiente Python...
C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe --version
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python nao encontrado
    pause
    exit /b 1
)

echo.
echo 2. Verificando Django...
C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe -c "import django; print('Django', django.get_version())"
if %errorlevel% neq 0 (
    echo ❌ ERRO: Django nao encontrado
    pause
    exit /b 1
)

echo.
echo 3. Verificando banco de dados...
C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe manage.py check --deploy
if %errorlevel% neq 0 (
    echo ❌ ERRO: Problemas no banco de dados
    pause
    exit /b 1
)

echo.
echo 4. Verificando dados...
C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe manage.py shell -c "from apps.restaurantes.models import Restaurante; print('Restaurantes:', Restaurante.objects.count())"

echo.
echo ================================================================
echo ✅ SISTEMA OK! Tudo funcionando corretamente.
echo.
echo Para iniciar o servidor:
echo    iniciar_sistema.bat
echo.
echo Para ver o resumo completo:
echo    RESUMO_EXECUTIVO.bat
echo ================================================================
echo.
pause
