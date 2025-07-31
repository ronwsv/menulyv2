@echo off
title Comandos Uteis - Sistema Menuly
echo.
echo ================================================================
echo                    COMANDOS UTEIS - MENULY
echo ================================================================
echo.
echo 1. Iniciar servidor
echo    iniciar_sistema.bat
echo.
echo 2. Popular dados novamente
echo    C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe manage.py popular_dados
echo.
echo 3. Criar superusuario
echo    C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe manage.py createsuperuser
echo.
echo 4. Fazer migracoes
echo    C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe manage.py makemigrations
echo    C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe manage.py migrate
echo.
echo 5. Shell Django
echo    C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe manage.py shell
echo.
echo 6. Coletar arquivos estaticos
echo    C:\Users\ron\Documents\other\projects\menuly\.venv\Scripts\python.exe manage.py collectstatic
echo.
echo ================================================================
echo.
pause
