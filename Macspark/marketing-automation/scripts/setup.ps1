# Script de setup completo do Marketing Automation Platform
# Versão Windows PowerShell

Write-Host "🚀 Setup Marketing Automation Platform" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Criar .env
Write-Host "📝 Configurando variáveis de ambiente..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item "env.template" ".env"
    Write-Host "✅ .env criado" -ForegroundColor Green
    Write-Host "⚠️  IMPORTANTE: Configure suas credenciais em .env" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  .env já existe. Pulando..." -ForegroundColor Yellow
}
Write-Host ""

# 2. Gerar API keys
Write-Host "🔐 Gerando API keys..." -ForegroundColor Yellow
function Generate-RandomKey {
    $bytes = New-Object byte[] 32
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    return [Convert]::ToBase64String($bytes) -replace '[/+=]', ''
}

$ANALYTICS_KEY = Generate-RandomKey
$SECRET_KEY = Generate-RandomKey
$SUPERSET_KEY = Generate-RandomKey

Write-Host ""
Write-Host "📋 API Keys geradas (adicione em .env):" -ForegroundColor Cyan
Write-Host "----------------------------------------"
Write-Host "ANALYTICS_API_KEY=$ANALYTICS_KEY"
Write-Host "SECRET_KEY=$SECRET_KEY"
Write-Host "SUPERSET_SECRET_KEY=$SUPERSET_KEY"
Write-Host "----------------------------------------"
Write-Host ""

# 3. Instalar shared package
Write-Host "📦 Instalando pacote compartilhado..." -ForegroundColor Yellow
Set-Location shared
pip install -e . --quiet
Set-Location ..
Write-Host "✅ Pacote compartilhado instalado" -ForegroundColor Green
Write-Host ""

# 4. Criar redes Docker
Write-Host "🐳 Criando redes Docker..." -ForegroundColor Yellow
docker network create marketing-net 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Rede já existe" -ForegroundColor Yellow
}
Write-Host ""

# 5. Build containers
Write-Host "🔨 Building containers (isso pode demorar)..." -ForegroundColor Yellow
docker-compose -f docker-compose.integrated.yml build
Write-Host "✅ Containers buildados" -ForegroundColor Green
Write-Host ""

# 6. Inicializar banco
Write-Host "💾 Inicializando banco de dados..." -ForegroundColor Yellow
docker-compose -f docker-compose.integrated.yml up -d postgres
Start-Sleep -Seconds 10
Write-Host "✅ PostgreSQL inicializado" -ForegroundColor Green
Write-Host ""

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "✅ Setup completo!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Edite .env e adicione suas credenciais"
Write-Host "2. Execute: docker-compose -f docker-compose.integrated.yml up -d"
Write-Host "3. Acesse: http://localhost:8000/docs"
Write-Host "4. Valide: python scripts/validate-integration.py"
Write-Host ""

