#!/bin/bash
# Script para reiniciar o servidor Django

echo "🔄 Reiniciando servidor Django..."
cd /workspaces/tsi-2025.2-ta3-petshop
docker-compose restart web

echo "⏳ Aguardando 5 segundos..."
sleep 5

echo "✅ Verificando status..."
docker-compose ps | grep web

echo ""
echo "🌐 Servidor deve estar disponível em:"
echo "   https://urban-guacamole-97669rr7vjjw3757w-8000.app.github.dev"
echo ""
echo "✅ Correção aplicada: LOGIN_URL = '/users/login/'"
