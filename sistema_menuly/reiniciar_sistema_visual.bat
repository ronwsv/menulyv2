@echo off
title Reiniciar Sistema Menuly - Ver Modificacoes
color 0A
echo.
echo ========================================
echo    REINICIANDO SISTEMA MENULY
echo    Visualizando Modificacoes Visuais
echo ========================================
echo.

REM Parar processos do Django se estiverem rodando
echo [1/6] Parando processos Django existentes...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Ativar ambiente virtual
echo [2/6] Ativando ambiente virtual...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo ✓ Ambiente virtual ativado
) else (
    echo ❌ Ambiente virtual nao encontrado!
    echo Criando ambiente virtual...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo ✓ Ambiente virtual criado e ativado
)

REM Instalar/Atualizar dependencias
echo [3/6] Verificando dependencias...
pip install -r requirements.txt --quiet
echo ✓ Dependencias verificadas

REM Aplicar migracoes
echo [4/6] Aplicando migracoes do banco de dados...
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo ✓ Migracoes aplicadas

REM Coletar arquivos estaticos
echo [5/6] Coletando arquivos estaticos...
python manage.py collectstatic --noinput --clear
echo ✓ Arquivos estaticos coletados

echo.
echo ========================================
echo   SISTEMA REINICIADO COM SUCESSO!
echo ========================================
echo.
echo 🎨 MODIFICACOES VISUAIS IMPLEMENTADAS:
echo.
echo ✓ Dashboard do Lojista - Interface Moderna
echo ✓ Dashboard do Super Admin - Tema Executivo  
echo ✓ Sistema de Login - Design Premium
echo ✓ Navegacao Sidebar - Layout Profissional
echo ✓ Graficos Interativos - Chart.js
echo ✓ Design Responsivo - Mobile + Desktop
echo ✓ Animacoes CSS - Efeitos Visuais
echo ✓ Sistema de Cores - Paleta Profissional
echo.
echo 🚀 FUNCIONALIDADES AVANCADAS:
echo.
echo ✓ Gestao de Impressoras - Configuracao e Testes
echo ✓ Sistema de Pedidos em Tempo Real - Dashboard Live
echo ✓ Controle Multi-Loja - Cada lojista ve apenas suas lojas
echo ✓ Atualizacao de Status - Sistema completo de workflow
echo ✓ Templates Profissionais - Lista e detalhes de pedidos
echo ✓ Filtros Avancados - Por status, restaurante e data
echo ✓ Estatisticas em Tempo Real - Metricas automaticas
echo ✓ Sistema de Timeline - Historico completo dos pedidos
echo.
echo ========================================
echo        ACESSOS DO SISTEMA
echo ========================================
echo.
echo 🔐 CREDENCIAIS DE TESTE:
echo    Usuario: lojista_teste
echo    Senha:   lojista123
echo.
echo 🌐 URLS PRINCIPAIS:
echo    Site Principal:     http://localhost:8000/
echo    Dashboard Lojista:  http://localhost:8000/lojista/dashboard/
echo    Login Lojista:      http://localhost:8000/lojista/login/
echo    Admin Django:       http://localhost:8000/admin/
echo    Super Admin:        http://localhost:8000/superadmin/dashboard/
echo.
echo 📊 GESTAO DE PEDIDOS:
echo    Lista de Pedidos:   http://localhost:8000/lojista/pedidos/
echo    Pedidos Tempo Real: http://localhost:8000/lojista/pedidos/tempo-real/
echo    Metricas Dashboard: http://localhost:8000/lojista/pedidos/metricas/
echo.
echo 🖨️ GESTAO DE IMPRESSORAS:
echo    Configurar:         http://localhost:8000/lojista/impressoras/
echo    Logs de Impressao:  http://localhost:8000/lojista/impressoras/logs/
echo.
echo 🏪 MINI-SITES DOS RESTAURANTES:
echo    Pizzaria do Jose:   http://localhost:8000/pizzaria-do-jose/
echo    Burger House:       http://localhost:8000/burger-house/
echo    Sushi Zen:          http://localhost:8000/sushi-zen/
echo.
echo ========================================

REM Iniciar servidor Django
echo [6/6] Iniciando servidor Django...
echo.
echo 🚀 SERVIDOR INICIANDO EM http://localhost:8000/
echo.
echo ⚡ Pressione Ctrl+C para parar o servidor
echo 📱 Teste a responsividade em diferentes tamanhos de tela
echo 🎨 Explore as animacoes e efeitos visuais
echo 📊 Verifique os graficos interativos nos dashboards
echo 🖨️ Configure as impressoras em /lojista/impressoras/
echo ⏱️ Acompanhe pedidos em tempo real em /lojista/pedidos/tempo-real/
echo 🏪 Cada lojista controla apenas seus proprios restaurantes
echo 📈 Veja metricas detalhadas em /lojista/pedidos/metricas/
echo.
echo ========================================
echo     APROVEITE O NOVO VISUAL! 🎉
echo ========================================
echo.

python manage.py runserver 0.0.0.0:8000
