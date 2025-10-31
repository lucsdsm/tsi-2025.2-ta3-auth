#!/bin/bash

echo "🚀 Iniciando setup do PetShop..."

# Aguardar o PostgreSQL estar pronto
echo "⏳ Aguardando PostgreSQL..."
sleep 10

# Aplicar migrations
echo "📦 Aplicando migrations..."
python manage.py migrate --noinput

# Executar comando de inicialização de usuários
echo "👥 Inicializando usuários e configurações..."
python manage.py init_users

# Executar comando de inicialização de dados de pets
echo "🐾 Inicializando dados de pets..."
python manage.py init_data

# Iniciar servidor Django
echo "🚀 Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000
