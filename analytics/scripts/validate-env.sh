#!/bin/bash
# Script de validação de variáveis de ambiente (Linux/Mac)

echo "🔍 Validando variáveis de ambiente..."

REQUIRED_VARS=(
    "SUPABASE_URL"
    "SUPABASE_SERVICE_KEY"
    "META_ACCESS_TOKEN"
    "META_AD_ACCOUNT_ID"
)

MISSING=()

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING+=("$var")
    fi
done

if [ ${#MISSING[@]} -eq 0 ]; then
    echo "✅ Todas variáveis obrigatórias configuradas!"
    exit 0
else
    echo "❌ Variáveis faltando:"
    for var in "${MISSING[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "💡 Copie .env.example para .env e preencha os valores"
    exit 1
fi
