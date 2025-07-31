@echo off
title Menuly - Demonstracao Visual
color 0E
cls
echo.
echo ========================================
echo    MENULY - DEMONSTRACAO VISUAL
echo    Sistema de Delivery Multi-Restaurante
echo ========================================
echo.

REM Verificar se o servidor esta rodando
echo Verificando servidor...
curl -s http://localhost:8000/ >nul 2>&1
if %errorlevel%==0 (
    echo ✓ Servidor esta rodando
) else (
    echo ❌ Servidor nao esta rodando
    echo Iniciando servidor primeiro...
    call .venv\Scripts\activate.bat
    start "" python manage.py runserver 0.0.0.0:8000
    echo Aguardando servidor iniciar...
    timeout /t 5 /nobreak >nul
)

echo.
echo ========================================
echo       TOUR VISUAL DO SISTEMA
echo ========================================
echo.
echo Abrindo demonstracao das interfaces...
echo.

REM Abrir paginas em sequencia para demonstracao
echo [1] Abrindo site principal...
start "" http://localhost:8000/
timeout /t 3 /nobreak >nul

echo [2] Abrindo login do lojista...
start "" http://localhost:8000/lojista/login/
timeout /t 3 /nobreak >nul

echo [3] Abrindo dashboard do lojista...
start "" "http://localhost:8000/lojista/login/?next=/lojista/dashboard/"
timeout /t 3 /nobreak >nul

echo [4] Abrindo mini-site da Pizzaria...
start "" http://localhost:8000/pizzaria-do-jose/
timeout /t 3 /nobreak >nul

echo [5] Abrindo mini-site do Burger House...
start "" http://localhost:8000/burger-house/
timeout /t 3 /nobreak >nul

echo [6] Abrindo admin do Django...
start "" http://localhost:8000/admin/
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo         PONTOS DE DESTAQUE
echo ========================================
echo.
echo 🎨 VISUAIS IMPLEMENTADOS:
echo    ✓ Interface moderna com gradientes
echo    ✓ Sidebar responsiva com animacoes
echo    ✓ Cards com hover effects
echo    ✓ Graficos interativos Chart.js
echo    ✓ Sistema de cores profissional
echo    ✓ Layout mobile-first
echo    ✓ Tipografia Poppins
echo    ✓ Animacoes CSS suaves
echo.
echo 🚀 FUNCIONALIDADES:
echo    ✓ Multi-restaurante (White Label)
echo    ✓ Dashboard com metricas
echo    ✓ Sistema de pedidos
echo    ✓ Gestao de produtos
echo    ✓ Autenticacao segura
echo    ✓ Admin personalizado
echo.
echo 📱 RESPONSIVIDADE:
echo    ✓ Desktop (1920px+)
echo    ✓ Laptop (1366px)
echo    ✓ Tablet (768px)
echo    ✓ Mobile (375px)
echo.
echo ========================================
echo        CREDENCIAIS DE TESTE
echo ========================================
echo.
echo 👤 LOJISTA:
echo    Usuario: lojista_teste
echo    Senha:   lojista123
echo.
echo 👑 SUPER ADMIN:
echo    Usuario: admin
echo    Senha:   admin123
echo.
echo 🏪 RESTAURANTES ATIVOS:
echo    - Pizzaria do Jose
echo    - Burger House  
echo    - Sushi Zen
echo.
echo ========================================
echo     TESTE AS FUNCIONALIDADES!
echo ========================================
echo.
echo 1. Faca login no painel do lojista
echo 2. Explore o dashboard interativo
echo 3. Teste a responsividade (F12 no browser)
echo 4. Visite os mini-sites dos restaurantes
echo 5. Verifique as animacoes e efeitos
echo 6. Teste o sistema de navegacao
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
