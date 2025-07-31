@echo off
title Menuly - Desenvolvimento Rapido
color 0B
echo.
echo =====================================
echo     MENULY - INICIO RAPIDO
echo =====================================
echo.

REM Ativar ambiente e iniciar servidor
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo Iniciando servidor Django...
echo.
echo 🚀 Servidor rodando em: http://localhost:8000/
echo.
echo 🔐 Login Lojista: lojista_teste / lojista123
echo 📊 Dashboard: http://localhost:8000/lojista/dashboard/
echo.
echo Pressione Ctrl+C para parar
echo.

python manage.py runserver 0.0.0.0:8000
