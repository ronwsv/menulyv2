#!/bin/bash

echo "🚀 Configurando Menuly v2..."

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
cd sistema_menuly
python -m venv .venv

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r ../requirements.txt

# Migrations
echo "🗄️ Configurando banco de dados..."
python manage.py migrate

# Criar superusuário (opcional)
echo "👤 Deseja criar um superusuário? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Executar servidor
echo "🌟 Iniciando servidor de desenvolvimento..."
echo "Acesse: http://localhost:8000"
python manage.py runserver
