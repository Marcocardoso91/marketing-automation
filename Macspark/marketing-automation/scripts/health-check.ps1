# Health check de todos os serviços
# Versão Windows PowerShell

Write-Host "🔍 Verificando saúde dos serviços..." -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

function Test-Service {
    param (
        [string]$name,
        [string]$url
    )
    
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $name" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ $name (não respondendo)" -ForegroundColor Red
        return $false
    }
}

# Verificar serviços
Test-Service "Agent API" "http://localhost:8000/health"
Test-Service "Metrics Endpoint" "http://localhost:8000/api/v1/metrics/health"
Test-Service "Superset" "http://localhost:8088/health"

Write-Host ""
Write-Host "🐳 Docker Containers:" -ForegroundColor Cyan
docker-compose -f docker-compose.integrated.yml ps

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Para logs: docker-compose -f docker-compose.integrated.yml logs -f"

